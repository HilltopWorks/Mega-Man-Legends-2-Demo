import os
from pathlib import Path
import sys


def uncompress(file_path, start_offset):
    
    comp_file = open(file_path, "rb")
    
    comp_file.seek(start_offset)
    
    file_type = int.from_bytes(comp_file.read(4), "little")
    
    
    assert file_type == 3, "ERROR, " + file_path + " " + hex(start_offset) + " IS NOT A COMPRESSED FILE"
    
    uncompressed_size = int.from_bytes(comp_file.read(4), "little")
    sectors_to_next = int.from_bytes(comp_file.read(4), "little")
    
    clut_x = int.from_bytes(comp_file.read(2), "little")
    clut_y = int.from_bytes(comp_file.read(2), "little")
    clut_w = int.from_bytes(comp_file.read(2), "little")
    clut_h = int.from_bytes(comp_file.read(2), "little")
    
    pxl_x = int.from_bytes(comp_file.read(2), "little")
    pxl_y = int.from_bytes(comp_file.read(2), "little")
    pxl_w = int.from_bytes(comp_file.read(2), "little")
    pxl_h = int.from_bytes(comp_file.read(2), "little")
    
    comp_file.seek(start_offset + 0x24)
    
    comp_cursor = start_offset + int.from_bytes(comp_file.read(2), "little") + 0x30
    control_cursor = start_offset + 0x30
    
    output_size = 0
    out_buffer = b""
    ref_window_cursor = 0
    
    for n in range((comp_cursor - control_cursor) //4):
        comp_file.seek(control_cursor)
        control_block = int.from_bytes(comp_file.read(4), "little")
        control_cursor += 4
        
        for bit_number in reversed(range(32)):
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
                    continue
                
                ref_size   = (ref_block & 0b111) + 2
                ref_offset = (ref_block & 0b1111111111111000) >> 3
                
                
                for x in range(ref_size):
                    ref_start = ref_window_cursor + ref_offset + x*2
                    out_buffer += out_buffer[ref_start:ref_start + 2]
                
                output_size += ref_size*2
                
    out_buffer = out_buffer[0:uncompressed_size]
    
    
    return out_buffer

def unpack_file(src_path, out_dir):
    dat_file = open(src_path, "rb")
    
    cursor = 0
    
    os.makedirs(out_dir, exist_ok=True)
    
    while cursor < os.stat(src_path).st_size - 0x800:
        dat_file.seek(cursor)
        
        file_type = int.from_bytes(dat_file.read(4), "little")
        file_size = int.from_bytes(dat_file.read(4), "little")
        sectors_to_next = int.from_bytes(dat_file.read(4), "little")
        load_address = int.from_bytes(dat_file.read(4), "little")
        
        out_stem = Path(src_path).stem + "-{0:#0{1}x}".format(cursor,10) + "-" + str(file_type)
        
        if file_type == 3:
            out_stem += ".uncomp"
        
        out_path = os.path.join(out_dir, out_stem + ".bin")
        out_file = open(out_path, 'wb')
        
        if file_type == 3:
            print("Uncompressing", out_stem)
            out_file.write(uncompress(src_path, cursor))
        else:
            print("Exporting", out_stem)
            dat_file.seek(cursor + 0x30)
            out_file.write(dat_file.read(file_size))
        
        out_file.close()
        
        cursor += sectors_to_next*0x800
    
    return

def unpack_all():
    os.makedirs("unpack\\DAT", exist_ok=True)
    os.makedirs("unpack\\PLDAT", exist_ok=True)
    
    files = Path("src\\DAT").glob('*.bin')
    for file in files:
        unpack_file(file, os.path.join("unpack\\DAT\\", Path(file).stem))
        
    files = Path("src\\PLDAT").glob('*.bin')
    for file in files:
        unpack_file(file, os.path.join("unpack\\PLDAT\\", Path(file).stem))
    
    return

#buf = uncompress("src\\DAT\\ST29T.BIN", 0x12800)
#f = open("test.bin", "wb")
#f.write(buf)
#f.close()

#unpack_file("src\\DAT\\ST29T.BIN", "test")

unpack_all()