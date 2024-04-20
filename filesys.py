import os
import shutil
from pathlib import Path
import math
import sys
import subprocess
import jpsxdec
import filecmp

build_path = "roll_build\\ROCKMAN.bin"
idx_path = "roll.idx"
jpsxdec_path = "jpsxdec.jar"

LBA_addr = 0x8006024C
base_addr = 0x8000F800

HEADER_SIZE = 0x30

def uncompress(file_path, start_offset):

    comp_file = open(file_path, "rb")
    comp_file.seek(start_offset)

    file_type = int.from_bytes(comp_file.read(4), "little") #0
    assert file_type == 3, "ERROR, " + file_path + " " + hex(start_offset) + " IS NOT A COMPRESSED FILE"
    
    uncompressed_size = int.from_bytes(comp_file.read(4), "little") #4
    sectors_to_next = int.from_bytes(comp_file.read(4), "little") #8
    
    clut_x = int.from_bytes(comp_file.read(2), "little") #A
    clut_y = int.from_bytes(comp_file.read(2), "little") #C
    clut_w = int.from_bytes(comp_file.read(2), "little") #E
    clut_h = int.from_bytes(comp_file.read(2), "little") #10
    
    pxl_x = int.from_bytes(comp_file.read(2), "little") #12
    pxl_y = int.from_bytes(comp_file.read(2), "little") #14
    pxl_w = int.from_bytes(comp_file.read(2), "little") #16
    pxl_h = int.from_bytes(comp_file.read(2), "little") #18
    
    comp_file.seek(start_offset + 0x24)
    
    comp_cursor = start_offset + int.from_bytes(comp_file.read(2), "little") + 0x30 #24
    control_cursor = start_offset + 0x30
    
    output_size = 0
    out_buffer = b""
    ref_window_cursor = 0
    end_reached = False
    FFFFs_left = uncompressed_size >> 0xD
    if uncompressed_size & 0x1FFF > 0:
        FFFFs_left += 1

    for n in range((comp_cursor - control_cursor) //4):
        if FFFFs_left == 0:
            break
        comp_file.seek(control_cursor)
        control_block = int.from_bytes(comp_file.read(4), "little")
        control_cursor += 4
        
        for bit_number in reversed(range(32)):
            if FFFFs_left == 0:
                break
            control_bit = control_block & (1 << bit_number)
            
            if control_bit == 0:
                #literal
                comp_file.seek(comp_cursor)
                out_buffer += comp_file.read(2)
                comp_cursor += 2
                output_size += 2
            else:
                #reference
                comp_file.seek(comp_cursor)
                ref_block = int.from_bytes(comp_file.read(2), "little")
                comp_cursor += 2
                if ref_block == 0xFFFF:
                    #Window push
                    ref_window_cursor += 0x2000
                    FFFFs_left -= 1
                    continue

                ref_size   = (ref_block & 0b111) + 2
                ref_offset = (ref_block & 0b1111111111111000) >> 3

                #print("Reference at offset %x, size %x" % (ref_offset, ref_size))

                if ref_offset + ref_size >= 0x2000:
                    #print("Reference overflow!!!")
                    pass

                for x in range(ref_size):
                    ref_start = ref_window_cursor + ref_offset + x*2
                    out_buffer += out_buffer[ref_start:ref_start + 2]
                
                output_size += ref_size*2

    print(hex(uncompressed_size), hex(output_size),  hex(ref_window_cursor), FFFFs_left)

    out_buffer = out_buffer[0:uncompressed_size]
    
    
    return out_buffer


def __common_start(sa, sb):
    """ returns the longest common substring from the beginning of sa and sb """
    def _iter():
        for a, b in zip(sa, sb):
            if a == b:
                yield a
            else:
                return

    return ''.join(_iter())

def compress(file_path, test=False):
    uncomp_file = open(file_path, "rb")
    uncomp_size = os.stat(file_path).st_size
    uncomp_bytes = uncomp_file.read()

    control_buffer = b""
    control_block_buffer = 0
    control_block_cursor = 31
    body_buffer = b""

    max_ref_size = (0b111 + 2)*2
    min_ref_size = 2

    bytes_compressed = 0
    ref_window_cursor = 0
    
    target_FFFFs = uncomp_size >> 0xD
    if uncomp_size & 0x1FFF != 0:
        target_FFFFs += 1

    current_FFFFs = 0

    #window_bytes = b''
    #window_bytes = uncomp_bytes[ref_window_cursor:ref_window_cursor + min(0x2000, bytes_compressed)]
    window_size = 0

    while bytes_compressed < uncomp_size:
        
        if control_block_cursor < 0:
            #Output control block and refresh
            control_buffer += control_block_buffer.to_bytes(4, "little")
            control_block_buffer = 0
            control_block_cursor = 31

        #search_bytes = uncomp_bytes[bytes_compressed:min(uncomp_size, bytes_compressed + max_ref_size)]

        if window_size > 0x2000:
            #Push window up if AND ONLY IF max window size reached (this is dumb but it's how they do it)
            ref_window_cursor += 0x2000
            body_buffer += b'\xFF\xFF'
            control_block_buffer = control_block_buffer | (1 << control_block_cursor)
            control_block_cursor -= 1
            window_size = 0
            current_FFFFs += 1

        if control_block_cursor < 0:
            #Output control block and refresh
            control_buffer += control_block_buffer.to_bytes(4, "little")
            control_block_buffer = 0
            control_block_cursor = 31

        ref_found = False
        for x in range(max_ref_size, min_ref_size, -2):
            #Look for reference
            search_word = uncomp_bytes[bytes_compressed: min(uncomp_size, bytes_compressed + x)]

            if x == max_ref_size:
                end_buffer = 4
            else:
                end_buffer = 2
            #window_bytes = uncomp_bytes[ref_window_cursor: min(uncomp_size, ref_window_cursor + window_size + len(search_word) - end_buffer)]
            window_bytes = uncomp_bytes[ref_window_cursor: min(uncomp_size, ref_window_cursor + window_size)]
            
            try:
                find_pos = window_bytes.index(search_word)

                #Reference found, output it
            except ValueError:
                #Reference not found, try next smaller size
                continue
            
            if x == max_ref_size and find_pos == 0x1FFF:
                #Can't code ref as 0xFFFF, reserved
                x = max_ref_size - 2

            ref_size_coded = (x//2) - 2
            ref_offset_coded = find_pos << 3
            ref_block = ref_offset_coded | ref_size_coded
            ref_bytes = ref_block.to_bytes(2, "little")
            body_buffer += ref_bytes
            
            assert control_block_cursor >= 0
            control_block_buffer = control_block_buffer | (1 << control_block_cursor)
            control_block_cursor -= 1

            window_size += x
            bytes_compressed += x
            ref_found = True
            break
        
        if ref_found:
            continue
        #No reference found, output literal
        body_buffer += uncomp_bytes[bytes_compressed: min(uncomp_size, bytes_compressed + 2)]
        window_size += 2
        bytes_compressed += 2
        control_block_cursor -= 1


    if control_block_cursor < 0:
        #Output control block and refresh
        control_buffer += control_block_buffer.to_bytes(4, "little")
        control_block_buffer = 0
        control_block_cursor = 31

    body_buffer = body_buffer + b"\xFF\xFF"
    control_block_buffer = control_block_buffer | (1 << control_block_cursor)
    control_block_cursor -= 1
    current_FFFFs += 1

    if current_FFFFs != target_FFFFs:
        if control_block_cursor < 0:
            #Output control block and refresh
            control_buffer += control_block_buffer.to_bytes(4, "little")
            control_block_buffer = 0
            control_block_cursor = 31

        body_buffer = body_buffer + b"\xFF\xFF"
        control_block_buffer = control_block_buffer | (1 << control_block_cursor)
        control_block_cursor -= 1
        current_FFFFs += 1
    
    assert current_FFFFs == target_FFFFs
    

    if control_block_cursor != 31:
        #write out final control block
        control_buffer += control_block_buffer.to_bytes(4, "little")
    else:
        assert False

    return control_buffer + body_buffer, len(control_buffer)

def unpack_file(src_path, out_dir):
    dat_file = open(src_path, "rb")
    
    cursor = 0
    
    os.makedirs(out_dir, exist_ok=True)
    
    while cursor < os.stat(src_path).st_size - 0x800:
        dat_file.seek(cursor)
        
        is_filesize_exception = isFilesizeException(src_path, cursor)

        file_type = int.from_bytes(dat_file.read(4), "little")
        file_size = int.from_bytes(dat_file.read(4), "little")
        sectors_to_next = int.from_bytes(dat_file.read(4), "little")
        
        out_stem = Path(src_path).stem + "-{0:#0{1}x}".format(cursor,10) + "-" + str(file_type)
        
        if file_type == 3:
            out_stem += ".uncomp"
        
        out_path = os.path.join(out_dir, out_stem + ".bin")
        out_file = open(out_path, 'wb')
        
        if file_type == 3:
            #print("Uncompressing", out_stem)
            out_file.write(uncompress(src_path, cursor))
        else:
            #print("Exporting", out_stem)
            dat_file.seek(cursor + 0x30)
            if is_filesize_exception:
                out_file.write(dat_file.read((sectors_to_next*0x800)-0x30))
            else:
                out_file.write(dat_file.read(file_size))
        
        out_file.close()
        
        cursor += sectors_to_next*0x800
    
    return

def unpack_USA(src_path, out_dir):
    dat_file = open(src_path, "rb")
    
    cursor = 0
    
    os.makedirs(out_dir, exist_ok=True)
    
    while cursor < os.stat(src_path).st_size - 0x800:
        dat_file.seek(cursor)
        
        is_filesize_exception = isFilesizeException(src_path, cursor)

        file_type = int.from_bytes(dat_file.read(4), "little")
        file_size = int.from_bytes(dat_file.read(4), "little")
        sectors_to_next = int.from_bytes(dat_file.read(4), "little")
        
        if file_size == 0:
            cursor += 0x800
            continue

        out_stem = Path(src_path).stem + "-{0:#0{1}x}".format(cursor,10) + "-" + str(file_type)
        
        if file_type == 3:
            out_stem += ".uncomp"
        
        out_path = os.path.join(out_dir, out_stem + ".bin")
        out_file = open(out_path, 'wb')
        
        if file_type == 3:
            #print("Uncompressing", out_stem)
            out_file.write(uncompress(src_path, cursor))
        else:
            #print("Exporting", out_stem)
            dat_file.seek(cursor + 0x30)
            if is_filesize_exception:
                out_file.write(dat_file.read((sectors_to_next*0x800)-0x30))
            else:
                out_file.write(dat_file.read(file_size))
        
        out_file.close()
        
        cursor += sectors_to_next*0x800
    
    return

def unpack_all(test=False):
    os.makedirs("unpack\\DAT", exist_ok=True)
    os.makedirs("unpack\\PLDAT", exist_ok=True)
    
    files = Path("src\\DAT").glob('*.bin')
    for file in files:
        out_folder =  "unpack\\DAT\\"
        if test:
            out_folder = os.path.join("test", out_folder)
        unpack_file(file, os.path.join(out_folder, Path(file).stem))
        
    files = Path("src\\PLDAT").glob('*.bin')
    for file in files:
        out_folder = "unpack\\DAT\\"
        if test:
            out_folder = os.path.join("test", out_folder)
        unpack_file(file, os.path.join(out_folder, Path(file).stem))
    
    return

def isFilesizeException(src_path, offset):
    src_file = open(src_path, "rb")
    src_file.seek(offset)

    file_type = int.from_bytes(src_file.read(4), "little")

    if file_type == 3:
        return False

    purported_size = int.from_bytes(src_file.read(4), "little")

    total_sectors = int.from_bytes(src_file.read(4), "little")

    min_size = total_sectors*0x800 - 0x7FF
    max_size = total_sectors*0x800
    if purported_size >= min_size and purported_size <= max_size:
        return False
    else:
        print(src_path, hex(offset), "is an exception. Type:", hex(file_type))
        return True

direct_copy_types = [5]
pack_types = [1,2,3]

def testUncompress(bytes, ref_file_path):
    test_comp_file = open("test\\comp_test_temp.bin", "wb")
    test_comp_file.write(bytes)
    test_comp_file.close()

    uncomp_bytes = uncompress("test\\comp_test_temp.bin", 0)
    test_uncomp_file = open("test\\uncomp_test_temp.bin", "wb")
    test_uncomp_file.write(uncomp_bytes)
    test_uncomp_file.close()
    
    assert filecmp.cmp("test\\uncomp_test_temp.bin", ref_file_path)

    
    
    return

def pack(folder, src_file_path, test=False):
    src_file = open(src_file_path, "rb")
    
    cursor = 0
    
    file_buffer = b""

    while cursor < os.stat(src_file_path).st_size - 0x800:
        src_file.seek(cursor)
        
        file_type = int.from_bytes(src_file.read(4), "little")
        src_file_size = int.from_bytes(src_file.read(4), "little")
        sectors_to_next = int.from_bytes(src_file.read(4), "little")

        if file_type not in pack_types:
            src_file.seek(cursor)
            file_buffer += src_file.read(sectors_to_next*0x800)
            cursor += sectors_to_next*0x800
            continue

        out_stem = Path(src_file_path).stem + "-{0:#0{1}x}".format(cursor,10) + "-" + str(file_type)    
       
        if file_type == 3:
            is_filesize_exception = False
        else:
            is_filesize_exception = isFilesizeException(src_file_path, cursor)

        if file_type == 3:
            out_stem += ".uncomp"
        
        in_file_path = os.path.join(folder, out_stem + ".bin")

        in_file = open(in_file_path, 'rb')
        
        if file_type == 3:
            in_bytes, control_offset = compress(in_file_path)
        else:
            in_bytes = in_file.read()
            
            control_offset = 0
        new_size = os.stat(in_file_path).st_size
        new_sectors = math.ceil((len(in_bytes) + HEADER_SIZE)/0x800)

        header_buffer = file_type.to_bytes(4, "little")
        if is_filesize_exception:
            header_buffer += src_file_size.to_bytes(4, "little")
            print("Exception File Type:", str(file_type))
        else:
            header_buffer += new_size.to_bytes(4, "little")
        header_buffer += new_sectors.to_bytes(4, "little")

        src_file.seek(cursor + 0xC)

        header_buffer += src_file.read(0x18)
        header_buffer += control_offset.to_bytes(2, "little")

        src_file.seek(cursor + 0x26)
        header_buffer += src_file.read(0xA)

        total_space = new_sectors*0x800

        file_buffer += header_buffer + in_bytes + bytes(total_space - (HEADER_SIZE + len(in_bytes)))

        if test and file_type == 3:
            print("Testing", in_file_path, is_filesize_exception)
            testUncompress(header_buffer + in_bytes, in_file_path)
        cursor += sectors_to_next*0x800

    return file_buffer + bytes(0x800)

def packDATs(target_folder):
    files = Path("src\\DAT").glob('*.bin')
    for file in files:
        print("Packing",file)
        in_folder = os.path.join("unpack_edit\\DAT", Path(file).stem)
        DAT_bytes = pack(os.path.join("unpack_edit\\DAT\\", Path(file).stem), file, test=False)

        out_path = file._str.replace("src", "src_edit")

        out_file = open(out_path, "wb")
        out_file.write(DAT_bytes)
        out_file.close()

        head, tail = os.path.split(file)
        shutil.copyfile(out_path,os.path.join(target_folder,  tail))

    return

def updateLBAs(exe_path):
    subprocess.call(["java", "-jar", jpsxdec_path, "-f" , build_path, "-x" ,idx_path])
    index = jpsxdec.parseIDX(idx_path)

    exe_file = open(exe_path, 'r+b')
    n_bin_files = 93

    XA_files = [93, 98, 101]

    for x in range(n_bin_files):
        exe_file.seek(x*0xC + LBA_addr - base_addr)
        size = int(index[x]["Size"])
        sectors = index[x]["Sectors"]

        sectors_split = sectors.split("-")
        start_sector = int(sectors_split[0])

        exe_file.write(start_sector.to_bytes(4, "little"))
        exe_file.write(size.to_bytes(4, "little"))

    for x in XA_files:
        exe_file.seek(x*0xC + LBA_addr - base_addr)
        size = int(index[x]["Size"])
        sectors = index[x]["Sectors"]

        sectors_split = sectors.split("-")
        start_sector = int(sectors_split[0])

        exe_file.write(start_sector.to_bytes(4, "little"))
        #exe_file.write(size.to_bytes(4, "little"))
    return


def testPack():
    bytes = pack("unpack_edit\DAT\DEMO", "src\DAT\DEMO.BIN")
    out_test_file = open("test\\pack_test.bin", "wb")
    out_test_file.write(bytes)
    out_test_file.close()

    return


def testCompress():
    comp_bytes,comp_offset = compress("test\\DEMO-0x00003800-3.uncomp.bin")
    out_file = open("test\\DEMO_comp.bin", "wb")
    out_file.write(bytes.fromhex("03 00 00 00 00 81 00 00 06 00 00 00 00 01 FC 01 40 00 02 00 40 03 00 00 40 00 00 01 00 00 00 00 00 00 00 00 "))
    out_file.write((comp_offset).to_bytes(2, "little"))
    out_file.write(bytes.fromhex("00 00 00 00 00 00 00 00 00 00"))
    out_file.write(comp_bytes)
    out_file.close()

    uncomp_bytes = uncompress("test\\DEMO_comp.bin", 0)
    out_file = open("test\\DEMO_uncomp.bin", "wb")
    
    out_file.write(uncomp_bytes)
    out_file.close()


#packDATs("roll_build\\DAT")
#updateLBAs("roll_build\\SLPS_021.09")
#testCompress()
#unpack_all()
#packDATs("roll_build\\DAT")
#testPack()


#buf = uncompress("src\\DAT\\ST29T.BIN", 0x12800)
#f = open("test.bin", "wb")
#f.write(buf)
#f.close()
#unpack_USA(r"Mega Man Legends 2 (USA) (Demo)\src\DAT\LEGEND2.BIN", r"Mega Man Legends 2 (USA) (Demo)\unpack")
#unpack_all()
