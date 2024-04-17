import TextHill
import os
from pathlib import Path
import math
import shutil

chars1, vals1 = TextHill.readCharOrder("FONT\\font_order1.txt", 0, 0xF8)
chars2, vals2 = TextHill.readCharOrder("FONT\\font_order2.txt", 0xF800)
chars3, vals3 = TextHill.readCharOrder("FONT\\font_order3.txt", 0xF900)
chars4, vals4 = TextHill.readCharOrder("FONT\\font_order4.txt", 0xFA00)

stock_val_dict = vals1 | vals2 | vals3 | vals4
stock_char_dict = chars1 | chars2 | chars3 | chars4

stock_val_dict[0xFC] = "\n"
stock_char_dict["\n"] = 0xFC

chars1, vals1 = TextHill.readCharOrder("FONT\\font_order1_inject.txt", 0, 0xF8)
chars2, vals2 = TextHill.readCharOrder("FONT\\font_order2_inject.txt", 0xF800)
chars3, vals3 = TextHill.readCharOrder("FONT\\font_order3.txt", 0xF900)
chars4, vals4 = TextHill.readCharOrder("FONT\\font_order4.txt", 0xFA00)

inject_val_dict = vals1 | vals2 | vals3 | vals4
inject_char_dict = chars1 | chars2 | chars3 | chars4

inject_val_dict[0xFC] = "\n"
inject_char_dict["\n"] = 0xFC



file_header = "//FILE SET "
line_header = "//LINE "

text_files =   {"unpack\DAT\ST07\ST07-0x00012000-1.bin": 0,
                "unpack\DAT\ST20\ST20-0x00014800-1.bin": 0,
                "unpack\DAT\ST21\ST21-0x0000e000-1.bin": 0,
                "unpack\DAT\ST22\ST22-0x00018800-1.bin": 0,
                "unpack\DAT\ST23\ST23-0x0001d000-1.bin": 0,
                "unpack\DAT\ST24\ST24-0x00026800-1.bin": 0,
                "unpack\DAT\ST26\ST26-0x00014800-1.bin": 0,
                "unpack\DAT\ST27T\ST27T-0x00002000-1.bin":0,
                "unpack\DAT\ST28\ST28-0x00014000-1.bin": 0,
                "unpack\DAT\ST29\ST29-0x0000c800-1.bin": 0,
                "unpack\DAT\ST2001\ST2001-0x00014800-1.bin": 0,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|0": 0x7304,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|1": 0x9244,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|2": 0x932c,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|3": 0x9640,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|4": 0x96ac,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|5": 0x970c,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|6": 0x9768,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|7": 0x97C0,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|8": 0x9870,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|9": 0x98e8,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|10": 0x99c0,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|11": 0x9a48,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|12": 0x9abc,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|13": 0x9c84,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|14": 0x9cfc,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|15": 0x9d70,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|16": 0x9dd8,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|17": 0x9e40,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|18": 0x9e9c,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|19": 0x970c,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|20": 0x9ef0,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|21": 0x9f94,
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|22": 0x9ff0,

                "src\SLPS_021.09|0": 0x5372C,
                "src\SLPS_021.09|1": 0x52FB0,
                "src\SLPS_021.09|2": 0x533E0,
                "src\SLPS_021.09|3": 0x535D8,
                "src\SLPS_021.09|4": 0x52D30
                }


subsc_loads =  [
                {#0
                    "ptrs":[],
                    "upper":[0x801ea5b4, 0x801ebc18],
                    "lower":[0x801ea5b8, 0x801ebc20]
                },
                {#1
                    "ptrs":[],
                    "upper":[0x801e6c10, 0x801e6c20, 0x801e6dc0, 0x801eb608],
                    "lower":[0x801e6c14, 0x801e6c24, 0x801e6dc4, 0x801eb60c]
                },
                {#2
                    "ptrs":[],
                    "upper":[0x801e8cd8, 0x801e8d34, 0x801e8f48],
                    "lower":[0x801e8cdc, 0x801e8d38, 0x801e8f4c]
                },
                {#3
                    "ptrs":[0x801f0874, 0x801f087C, 0x801f0884],
                    "upper":[],
                    "lower":[]
                },
                {#4
                    "ptrs":[0x801f08b4],
                    "upper":[],
                    "lower":[]
                },
                {#5
                    "ptrs":[0x801eff0c],
                    "upper":[],
                    "lower":[]
                },
                {#6
                    "ptrs":[],
                    "upper":[],
                    "lower":[]
                },
                {#7
                    "ptrs":[0x801f08ac],
                    "upper":[],
                    "lower":[]
                },
                {#8
                    "ptrs":[],
                    "upper":[],
                    "lower":[]
                },
                {#9
                    "ptrs":[0x801f094c],
                    "upper":[],
                    "lower":[]
                },
                {#10
                    "ptrs":[0x801f08fc],
                    "upper":[],
                    "lower":[]
                },
                {#11
                    "ptrs":[0x801f08cc],
                    "upper":[],
                    "lower":[]
                },
                {#12
                    "ptrs":[],
                    "upper":[0x801e8bf0,0x801e8c28],
                    "lower":[0x801e8bf8,0x801e8c30]
                },
                {#13
                    "ptrs":[0x801f090c],
                    "upper":[],
                    "lower":[]
                },
                {#14
                    "ptrs":[0x801f08e4],
                    "upper":[],
                    "lower":[]
                },
                {#15
                    "ptrs":[0x801f08ec, 0x801f08f4],
                    "upper":[],
                    "lower":[]
                },
                {#16
                    "ptrs":[0x801f095c],
                    "upper":[],
                    "lower":[]
                },
                {#17
                    "ptrs":[0x801f0934],
                    "upper":[],
                    "lower":[]
                },
                {#18
                    "ptrs":[0x801f093c],
                    "upper":[],
                    "lower":[]
                },
                {#19
                    "ptrs":[0x801f089c],
                    "upper":[],
                    "lower":[]
                },
                {#20
                    "ptrs":[0x801f091c],
                    "upper":[0x801e9834],
                    "lower":[0x801e9838]
                },
                {#21
                    "ptrs":[0x801f096c],
                    "upper":[],
                    "lower":[]
                },
                {#22
                    "ptrs":[0x801f0974],
                    "upper":[],
                    "lower":[]
                }
               ]

subsc_bin_start = 0x801e6800
subsc_text_start = 0x801edb04
subsc_text_max = 0x2d6C


def get_subsc_addrs():
    for x in text_files:
        if "SUBS" not in x:
            continue

        offset = text_files[x]
        print(hex(offset + subsc_bin_start))

    return



#area_offset = 0x535D8

pause_text_loads = {
                    "upper":[0x8001b128],
                    "lower":[0x8001b130]
                    }

button_text_loads = {
                    "upper":[0x80041b54,0x80041be4],
                    "lower":[0x80041b58,0x80041be8]
                    }

area_text_loads = {
                    "upper":[0x80043030],
                    "lower":[0x80043034]
                    }

parts_text_loads = {
                    "upper":[0x80041990,0x800419dc,0x80043050],
                    "lower":[0x80041994,0x800419e0,0x80043054]
                    }
parts_text_loads_subsc = {
                    "upper":[0x801E6800 + 0x3D40,0x801E6800 + 0x51c4,0x801E6800 + 0x54e0],
                    "lower":[0x801E6800 + 0x3D44,0x801E6800 + 0x51c8,0x801E6800 + 0x54e4]
                    }

menu_text_loads = {
                    "ptrs":[0x80062678],
                    "upper":[],
                    "lower":[]
                    }
exe_text_start = 0x800627b0
exe_text_size_max = 0x190F




def make_control_code_list():
    for x in range(0x38):
        print(hex(x) + " : " + " ,")
    
    return

def convertString(bytes):
    string = TextHill.convertRawToText(stock_val_dict, bytes, b"\xFF")
    print(string)
    return string

def convertRaw(string):
    bytes, box_size = TextHill.convertTextToRaw(stock_char_dict, string, b"\xFF")
    print(bytes.hex())
    return bytes

def convertMSG(msg_file_path, start_offset):
    msg_file = open(msg_file_path, 'rb')
    buffer = "//FILE SET " + msg_file_path + "|" + hex(start_offset) + "\n\n"
    
    msg_file.seek(start_offset)
    
    string_offsets = []
    
    offset1 = int.from_bytes(msg_file.read(2), "little")
    
    string_offsets += [offset1]
    
    for x in range((offset1//2)-1):
        string_offsets += [int.from_bytes(msg_file.read(2), "little")]
        
    
    for x in range(len(string_offsets) - 1):
        string_start = string_offsets[x]
        string_end = string_offsets[x + 1]
        string_length = string_end - string_start
        
        msg_file.seek(string_start + start_offset)
        
        header_line = "//LINE " + str(x).zfill(3) + "\n"
        
        string_bytes = msg_file.read(string_length)
        string_text = TextHill.convertRawToText(stock_val_dict, string_bytes)
        
        reference_string = "//" + string_text.replace("\n", "\n//")
        
        buffer += header_line + reference_string + "\n" + string_text + "\n\n"
    
    print(buffer)
        
    
    return buffer

def extractText():
    buffer = ""
    for file_path in text_files:
        text_offset = text_files[file_path]
        file_path = file_path.split("|")[0]
        file_text = convertMSG(file_path, text_offset)
        buffer += file_text
    
    out_file = open("MML_text.txt", "w", encoding="UTF8")
    out_file.write(buffer)
    out_file.close()
    
    return

def injectTextToBin(text_file_path):
    injected_bin = {}

    text_file = open(text_file_path, "r", encoding="utf8")
    text_blob = text_file.read()

    files = text_blob.split(file_header)

    for file_text in files[1:]:
        header_buffer = b""
        body_buffer = b""

        src_line = file_text.split("\n")[0].strip()
        src_path = src_line.split("|")[0]
        src_file = open(src_path, "rb")

        if "SLPS" in src_path or "SUBSCN" in src_path:
            file_offset = int(src_line.split("|")[1],16)
        else:
            file_offset = 0
        src_file.seek(file_offset)

        n_line_entries = (int.from_bytes(src_file.read(2), "little")//2)
        header_buffer += ((n_line_entries)*2).to_bytes(2, "little")

        lines = file_text.split(line_header)[1:]

        last_line = "-=PLACEHOLDER=-"

        for line in lines:
            string_buffer = ""
            broken_lines = line.split("\n")[1:]
            for broken_line in broken_lines:
                if broken_line.startswith("//"):
                    continue
                string_buffer += broken_line + "\n"

            string_buffer = string_buffer.rstrip()
            
            string_bytes, box_size = TextHill.convertTextToRaw(inject_char_dict, string_buffer)

            body_buffer += string_bytes
            line_offset = (len(body_buffer) + n_line_entries*2)
            header_buffer += line_offset.to_bytes(2, "little")
            last_line = string_buffer

        injected_bin[src_line] = header_buffer + body_buffer

    return injected_bin

FPS = 30

def timestampsToFrameCount(start, end):
    start_hour = int(start[0])
    start_minute = int(start[2:4])
    start_second = int(start[5:7])
    start_millisecond = int(start[8:10])

    end_hour = int(end[0])
    end_minute = int(end[2:4])
    end_second = int(end[5:7])
    end_millisecond = int(end[8:10])
    
    lifetime = (end_hour - start_hour)*60*60*FPS
    lifetime += (end_minute - start_minute)*60*FPS
    lifetime += (end_second - start_second)*FPS
    lifetime += int((end_millisecond - start_millisecond)*FPS/100)
    return lifetime

voice_file_header = "//Scene:"

def injectVoiceSub(text_file_path):
    text_file = open(text_file_path, "r", encoding="utf8")
    text_blob = text_file.read()

    files = text_blob.split(voice_file_header)

    for file_text in files[1:]:

        header_buffer = b""
        body_buffer = b""

        scripting_buffer = b""

        src_line = file_text.split("\n")[0].strip()
        inject_path = src_line.split(",")[0]
        src_path = inject_path.replace("unpack_edit", "unpack")

        shutil.copy(src_path, inject_path)

        scene_name = inject_path.split("/")[-2]

        lines = file_text.split("\n")[1:]

        inject_lines = []

        
        for line in lines:
            string_buffer = ""
            if line.startswith("//") or "Dialogue" not in line:
                continue

            string_buffer = line.split(",", 9)[-1].rstrip().replace("\\N", "\n")

            string_bytes, box_size = TextHill.convertTextToRaw(inject_char_dict, string_buffer)

            front_buffer = b"\x05\x00"
            
            unknown1 = b"\xfb\x29"
            unknownA = b"\xfb\x2d\x01"
            unknownB = b"\xfd\x00\x02\x00\x00"
            unknownC = b"\xfb\x0c"

            screen_width = 332
            start_X = int(screen_width/2 - (box_size[0]/2))
            start_Y = int(0xBE - box_size[1]/2)
            #box = b"\xfb\x06" + start_X.to_bytes(2, "big") + start_Y.to_bytes(2, "big") + math.ceil(box_size[0]/0xC).to_bytes(1, "little") + (0x10 | box_size[1]).to_bytes(1, "little")
            box = b"\xfb\x06" + start_X.to_bytes(2, "big") + start_Y.to_bytes(2, "big") + math.ceil(box_size[0]/0xC).to_bytes(1, "little") + (box_size[1]).to_bytes(1, "little")
            
            box_type = b"\xfb\x05\x01\x08"
            unknown2 = b"\xfb\x1d"

            instant_text = b"\xfb\x09\x00"
            single_speed_text = b"\xfb\x09\x01"
            slow_speed_text = b"\xfb\x09\xFF"

            start_timestamp = line.split(",")[1]
            end_timestamp = line.split(",")[2]

            ID_1 = int(line.split(",")[4], base=16)
            ID_2 = int(line.split(",")[5], base=16)
            ID_3 = int(line.split(",")[6], base=16)
            ID_4 = int(line.split(",")[7], base=16)

            frame_ID = ID_1 | (ID_2 << 8) | (ID_3 << 16) | (ID_4 << 24)
            start_frame = int(line.split(",")[8], base=16)

            scripting_buffer += frame_ID.to_bytes(4, "little")
            scripting_buffer += start_frame.to_bytes(4, "little")

            

            frame_lifetime = timestampsToFrameCount(start_timestamp, end_timestamp)
            
            pause = b"\xfb\x08" +  frame_lifetime.to_bytes(2, "big")
            lifetime = b"\xfb\x04" + frame_lifetime.to_bytes(2, "big")
            terminator = b"\xFF"
            #10{fb2d01}{fb0900}{fb06006200b40c11}{fb050108}You used the key!{fb0901}{fb08002d}{fd00020000}{fb0c}{fb260581}

            string_bytes = front_buffer + instant_text + unknown1 + box + box_type + unknown2 + string_bytes[:-1] + single_speed_text + lifetime + terminator

            inject_lines.append(string_bytes)

        header_buffer += ((len(inject_lines))*2).to_bytes(2, "little")
        body_buffer += inject_lines[0]
        
        for i in range(len(inject_lines)-1):
            cursor = len(body_buffer) + (len(inject_lines))*2
            header_buffer += cursor.to_bytes(2, "little")
            body_buffer += inject_lines[i+1]

        inject_file = open(scene_name + "_sub.bin", "wb")
        scripting_file = open(scene_name + "_scripting.bin", "wb")
        scripting_file.write(scripting_buffer + 0xFFFFFFFF.to_bytes(4, "little"))
        inject_file.write(header_buffer + body_buffer)
        scripting_file.close()
        inject_file.close()

    return

def applyLoad(address, loads, exe_file, exe_offset):


    address_hi = address >> 16
    address_lo = address & 0xFFFF
    
    if address_lo >= 0x8000:
        address_hi += 1

    for hi_addr in loads["upper"]:
        exe_file.seek(hi_addr - exe_offset)
        exe_file.write(address_hi.to_bytes(2, "little"))
    for lo_addr in loads["lower"]:
        exe_file.seek(lo_addr - exe_offset)
        exe_file.write(address_lo.to_bytes(2, "little"))

    if "ptrs" in loads:
        for ptr in loads["ptrs"]:
            exe_file.seek(ptr - exe_offset)
            exe_file.write(address.to_bytes(4, "little"))
    return

def injectAll(text_file_path, exe_path):
    injected_bins = injectTextToBin(text_file_path)

    for file_path in injected_bins:

        if "DAT" in file_path:
            #DAT file text
            target_path = file_path.replace("unpack", "unpack_edit")
            
            if "SUBSCN" in file_path:
                continue
                #target_file = open(target_path, "r+b")
                #assert len(injected_bins[file_path]) <= 0x1F3F
            else:
                target_file = open(target_path, "wb")
            target_offset = text_files[file_path]
            target_file.seek(target_offset)
            target_file.write(injected_bins[file_path])
            target_file.close()
    
    exe_pause_file = injected_bins["src\SLPS_021.09|0x52fb0"]
    if len(exe_pause_file) % 2 != 0:
        exe_pause_file += b"\x00"

    exe_buttons_file = injected_bins["src\SLPS_021.09|0x533e0"]
    if len(exe_buttons_file) % 2 != 0:
        exe_buttons_file += b"\x00"

    exe_area_file = injected_bins["src\SLPS_021.09|0x535d8"]
    if len(exe_area_file) % 2 != 0:
        exe_area_file += b"\x00"

    exe_parts_file = injected_bins["src\SLPS_021.09|0x5372C"]
    if len(exe_parts_file) % 2 != 0:
        exe_parts_file += b"\x00"

    exe_menu_file = injected_bins["src\SLPS_021.09|0x52d30"]
    if len(exe_menu_file) % 2 != 0:
        exe_menu_file += b"\x00"


    exe_blob = exe_pause_file + exe_buttons_file + exe_area_file + exe_parts_file + exe_menu_file
    assert len(exe_blob) <= exe_text_size_max
    print(len(exe_blob) - exe_text_size_max)

    exe_file = open(exe_path, "r+b")

    exe_file.seek(exe_text_start - 0x8000f800)
    exe_file.write(exe_blob)

    subscr_file = open("unpack_edit\\DAT\\SUBSCN00\\SUBSCN00-0x00000000-1.bin", "r+b")
    
    #applyLoad(exe_text_start                                                                   , pause_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file)                                             , button_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file) + len(exe_buttons_file)                     , area_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file) + len(exe_buttons_file) + len(exe_area_file), parts_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file) + len(exe_buttons_file) + len(exe_area_file), parts_text_loads_subsc, subscr_file, subsc_bin_start)
    applyLoad(exe_text_start + len(exe_pause_file) + len(exe_buttons_file) + len(exe_area_file) + len(exe_parts_file), menu_text_loads, exe_file, 0x8000f800)

    subsc_blob = b''
    subscr_sizes = []
    for x in range(len(subsc_loads)):
        offset = text_files["unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|" + str(x)]
        subsc_file = injected_bins["unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin|" + hex(offset)]
        if len(subsc_file) % 4 != 0:
            n_buffers = 4 - (len(subsc_file) % 4)
            subsc_file += b"\x00" * n_buffers
        subsc_blob += subsc_file
        subscr_sizes.append(len(subsc_file))

    assert len(subsc_blob) <= subsc_text_max

    #subscr_parent_file = open("src_edit\DAT\SUBSCN00.BIN", "r+b")
    #subscr_parent_file = open("unpack_edit\\DAT\\SUBSCN00\\SUBSCN00-0x00000000-1.bin", "r+b")
    
    subscr_file.seek(subsc_text_start - subsc_bin_start)
    subscr_file.write(subsc_blob)

    cursor = 0
    for x in range(len(subsc_loads)):
        applyLoad(subsc_text_start + cursor, subsc_loads[x], subscr_file, subsc_bin_start )
        cursor += subscr_sizes[x]
    
    injectVoiceSub("recieved\\MML_sub_text.txt")
    return

#injectVoiceSub("recieved\\MML_sub_text.txt")
#make_control_code_list()
#convertMSG("src\\DAT\\ST22.BIN", 0x18830)
#convertMSG("unpack\DAT\ST24\ST24-0x00026800-1.bin", 0)
#convertMSG(r"C:\dev\roll\unpack\DAT\ST27T\ST27T-0x00002000-1.bin", 0)
#convertMSG(r"C:\dev\roll\unpack\DAT\ST20\ST20-0x00014800-1.bin", 0)
#convertMSG(r"C:\dev\roll\unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin", 0x7304)
#convertMSG(r"unpack\DAT\ST27T\ST27T-0x00002000-1.bin", 0x0)
#convertMSG(r"src_edit\SLPS_021.09", 0x5372C)

#convertString(b"\xFA\x32\xF8\x3B\xFA\x56\xF9\x38\xF9\x22\xFA\x7B\x7C\xF9\xA4\xFA\x99\x5B\x6E\x5C")
#convertRaw("特殊式器")


#get_subsc_addrs()
#extractText()
#injectAll("recieved\\MML_text.txt", "src_edit\\SLPS_021.09")
#injectTextToBin("recieved\\MML_text.txt")