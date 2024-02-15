import TextHill
import os
from pathlib import Path

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
                "unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin": 0x7304,
                "src\SLPS_021.09|0": 0x5372C,
                "src\SLPS_021.09|1": 0x52FB0,
                "src\SLPS_021.09|2": 0x533E0,
                "src\SLPS_021.09|3": 0x535D8}

area_offset = 0x535D8

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

exe_text_start = 0x800627b0
exe_text_size_max = 0x190F

def make_control_code_list():
    for x in range(0x38):
        print(hex(x) + " : " + " ,")
    
    return

def convertRaw(string):
    bytes = TextHill.convertTextToRaw(stock_char_dict, string, b"\xFF")
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

        if "SLPS" in src_path:
            file_offset = int(src_line.split("|")[1],16)
        elif "SUBSCN" in src_path:
            file_offset = 0x7304
        else:
            file_offset = 0
        src_file.seek(file_offset)

        n_line_entries = (int.from_bytes(src_file.read(2), "little")//2)
        header_buffer += ((n_line_entries)*2).to_bytes(2, "little")

        lines = file_text.split(line_header)[1:]

        for line in lines:
            string_buffer = ""
            broken_lines = line.split("\n")[1:]
            for broken_line in broken_lines:
                if broken_line.startswith("//"):
                    continue
                string_buffer += broken_line + "\n"

            string_buffer = string_buffer.rstrip()

            string_bytes = TextHill.convertTextToRaw(inject_char_dict, string_buffer)
            body_buffer += string_bytes
            line_offset = (len(body_buffer) + n_line_entries*2)
            header_buffer += line_offset.to_bytes(2, "little")

        injected_bin[src_line] = header_buffer + body_buffer

    return injected_bin

def applyLoad(address, loads, exe_file, exe_offset):
    address_hi = address >> 16
    address_lo = address & 0xFFFF
    
    for hi_addr in loads["upper"]:
        exe_file.seek(hi_addr - exe_offset)
        exe_file.write(address_hi.to_bytes(2, "little"))
    for lo_addr in loads["lower"]:
        exe_file.seek(lo_addr - exe_offset)
        exe_file.write(address_lo.to_bytes(2, "little"))
    return

def injectAll(text_file_path, exe_path):
    injected_bins = injectTextToBin(text_file_path)

    for file_path in injected_bins:

        if "DAT" in file_path:
            #DAT file text
            target_path = file_path.replace("unpack", "unpack_edit")
            target_offset = text_files[file_path]
            if "SUBSCN" in file_path:
                target_file = open(target_path, "r+b")
                assert len(injected_bins[file_path]) <= 0x1F3F
            else:
                target_file = open(target_path, "wb")
            
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


    exe_blob = exe_pause_file + exe_buttons_file + exe_area_file + exe_parts_file
    assert len(exe_blob) <= exe_text_size_max

    exe_file = open(exe_path, "r+b")

    exe_file.seek(exe_text_start - 0x8000f800)
    exe_file.write(exe_blob)

    applyLoad(exe_text_start                                                                   , pause_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file)                                             , button_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file) + len(exe_buttons_file)                     , area_text_loads, exe_file, 0x8000f800)
    applyLoad(exe_text_start + len(exe_pause_file) + len(exe_buttons_file) + len(exe_area_file), parts_text_loads, exe_file, 0x8000f800)
    return


#make_control_code_list()
#convertMSG("src\\DAT\\ST22.BIN", 0x18830)
#convertMSG("unpack\DAT\ST24\ST24-0x00026800-1.bin", 0)
#convertMSG(r"C:\dev\roll\unpack\DAT\ST27T\ST27T-0x00002000-1.bin", 0)
#convertMSG(r"C:\dev\roll\unpack\DAT\ST20\ST20-0x00014800-1.bin", 0)
#convertMSG(r"C:\dev\roll\unpack\DAT\SUBSCN00\SUBSCN00-0x00000000-1.bin", 0x7304)
#convertMSG(r"unpack\DAT\ST27T\ST27T-0x00002000-1.bin", 0x0)
#convertMSG(r"src_edit\SLPS_021.09", 0x5372C)
#convertRaw("PAUSE")

#extractText()
injectAll("recieved\\MML_text.txt", "src_edit\\SLPS_021.09")
#injectTextToBin("recieved\\MML_text.txt")