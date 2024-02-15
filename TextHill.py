import os
import shutil
from pathlib import Path
import polib

raw_hex_start = "{"
raw_hex_end = "}"

FB_control_code_lengths =   {
                            0x00 :  0,
                            0x01 :  3,
                            0x02 :  1,
                            0x03 :  0,
                            0x04 :  2,
                            0x05 :  2,
                            0x06 :  6,
                            0x07 :  1,
                            0x08 :  2,
                            0x09 :  1,
                            0x0a :  1,
                            0x0b :  0,
                            0x0c :  0,
                            0x0d :  4,
                            0x0e :  1,
                            0x0f :  1,
                            0x10 :  5,
                            0x11 :  3,
                            0x12 :  2,
                            0x13 :  2,
                            0x14 :  3,
                            0x15 :  9,
                            0x16 :  11,
                            0x17 :  0,
                            0x18 :  0,
                            0x19 :  2,
                            0x1a :  3,
                            0x1b :  0,
                            0x1c :  0,
                            0x1d :  0,
                            0x1e :  2,
                            0x1f :  0,
                            0x20 :  1,
                            0x21 :  0,
                            0x22 :  1,
                            0x23 :  0,
                            0x24 :  0,
                            0x25 :  0,
                            0x26 :  2,
                            0x27 :  0,
                            0x28 :  4,
                            0x29 :  0,
                            0x2a :  2,
                            0x2b :  0,
                            0x2c :  1,
                            0x2d :  1,
                            0x2e :  1,
                            0x2f :  1,
                            0x30 :  1,
                            0x31 :  0,
                            0x32 :  1,
                            0x33 :  1,
                            0x34 :  2,
                            0x35 :  2,
                            0x36 :  2,
                            0x37 :  4
                            }

def readCharOrder(txt_path, start_val, max_entries = 0x100):
    #Converts a character map in a text file to a dictionary
    txt_file = open(txt_path, "r", encoding="utf8")
    
    all_chars = txt_file.read().replace("\n","")
    
    char_dict = {}
    val_dict = {}
    
    value_cursor = 0
    for char in all_chars:
        
        char_dict[char] = value_cursor + start_val
        val_dict[value_cursor + start_val] = char
        
        #print(char + "=" + "{0:#0{1}x}".format(value_cursor + start_val,6) )
        value_cursor += 1
        
        if value_cursor == max_entries:
            break
        
    return char_dict, val_dict


def convertRawToText(dict, raw, escape_char = 0xFF):
    '''binary -> string'''
    string = ""
    bytes_read = 0
    
    while True:
        if bytes_read >= len(raw):
            break
        val = int.from_bytes(raw[bytes_read:bytes_read + 1], byteorder="little")
        
        
        if val == 0xFB:
            control_code_type = int.from_bytes(raw[bytes_read+1:bytes_read + 2], byteorder="little")
            
            
            try:
                control_code_length = FB_control_code_lengths[control_code_type]
            except KeyError:
                assert False, "UNHANDLED CONTROL CODE!!!"
            
            control_bytes = raw[bytes_read:bytes_read + control_code_length + 2]
            char = raw_hex_start + control_bytes.hex() + raw_hex_end
            bytes_read += control_code_length + 2
        elif val == 0xFD:
            control_bytes = raw[bytes_read:bytes_read + 5]
            char = raw_hex_start + control_bytes.hex() + raw_hex_end
            bytes_read += 5
        elif val == 0xFE:
            byte_1 = int.from_bytes(raw[bytes_read + 1:bytes_read + 2], byteorder="little")
            
            
            if byte_1 >= 0xF8:
                byte_2 = int.from_bytes(raw[bytes_read + 2:bytes_read + 3], byteorder="little")
                char_val = (byte_1 << 8) + byte_2
                bytes_read += 3
            else:
                char_val = byte_1
                bytes_read += 2
            internal_char = dict[char_val]
            
            n_skip_bytes = int.from_bytes(raw[bytes_read:bytes_read + 1], byteorder="little") + 1
            
            skipped_bytes = raw[bytes_read + 1:bytes_read + 1 + n_skip_bytes]
            
            bytes_read += n_skip_bytes + 1
            
            n_skipped_bytes_string = hex(n_skip_bytes).replace("0x","").zfill(2)
            
            #char = "{" + internal_char + "-FE" + n_skipped_bytes_string + skipped_bytes.hex() + "}"
            char = internal_char
        
        elif val == escape_char:
            return string
        else:
            
            if val >= 0xF8 and val <= 0xFA:
                byte_2 = int.from_bytes(raw[bytes_read + 1:bytes_read + 2], byteorder="little")
                val = (val << 8) + byte_2
                bytes_read += 1
            try:
                char = dict[val]
            except KeyError:
                char = raw_hex_start + hex(val) + raw_hex_end
            bytes_read += 1
        
        string += char
    return string



def convertTextToRaw(dict, text, terminator = b"\xFF"):
    '''string -> binary'''
    buffer = b""

    while True:
        if len(text) == 0:
            break
        
        if text.startswith(raw_hex_start):
            code_length = text.find(raw_hex_end) + len(raw_hex_start)
            code = text[:code_length]
            code = code.replace(raw_hex_end,"").replace(raw_hex_start, "")
            
            buffer += bytearray.fromhex(code)
            
            chars_read = code_length
            text = text[chars_read:]
            continue
        
        try:
            val = dict[text[0]]
            if val > 0xFF:
                buffer += val.to_bytes(2, byteorder="big")
            else:
                buffer += val.to_bytes(1, byteorder="big")
                
            chars_read = 1
        except KeyError:
            print("INSERTION ERROR!!! CHAR: -" + text[0] + "- in " + text)
            chars_read = 1

        text = text[chars_read:]
    
    return buffer + terminator



