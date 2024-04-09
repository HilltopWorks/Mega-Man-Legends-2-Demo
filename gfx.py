import ImageHill
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont


##### Font

font_pxl =            {
                            "PXL_FILE":r"C:\dev\roll\unpack\DAT\INIT\INIT-0x00013800-2.bin",
                            "PXL_OFFSET":0x7d0,
                            "WIDTH":256,
                            "HEIGHT":0xFC,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

font_clut1 =          {
                            "CLUT_FILE":r"C:\dev\roll\unpack\DAT\INIT\INIT-0x00013800-2.bin",
                            "CLUT_OFFSET":0x0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

font_clut2 =          {
                            "CLUT_FILE":r"C:\dev\roll\unpack\DAT\INIT\INIT-0x00013800-2.bin",
                            "CLUT_OFFSET":0x100,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

font_pxl_inject_1 = {
                            "PXL_FILE":r"font\\INIT-0x00013800-2_1.bin",
                            "PXL_OFFSET":0x7d0,
                            "WIDTH":256,
                            "HEIGHT":0xFC,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
font_pxl_inject_2 = {
                            "PXL_FILE":r"font\\INIT-0x00013800-2_2.bin",
                            "PXL_OFFSET":0x7d0,
                            "WIDTH":256,
                            "HEIGHT":0xFC,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

test1C =          {
                            "CLUT_FILE":r"unpack\DAT\ST00T\ST00T-0x0001a800-3.uncomp.bin",
                            "CLUT_OFFSET":0xC0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }


##### Subscreens

subscC =          {
                            "CLUT_FILE":r"unpack\DAT\GAME\GAME-0x00030800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }



subsc1P = {
                            "PXL_FILE":r"unpack\DAT\SUBSCN06\SUBSCN06-0x00000000-2.bin",
                            "PXL_OFFSET":0x3d0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

subsc2P = {
                            "PXL_FILE":r"unpack\DAT\SUBSCN03\SUBSCN03-0x00001800-2.bin",
                            "PXL_OFFSET":0x9D0,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }



subsc3P = {
                            "PXL_FILE":r"unpack\DAT\SUBSCN04\SUBSCN04-0x00000000-2.bin",
                            "PXL_OFFSET":0x9D0,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

subsc4P = {
                            "PXL_FILE":r"unpack\DAT\GAME\GAME-0x00030800-3.uncomp.bin",
                            "PXL_OFFSET":0x300,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

###### Subscreens USA

subscP_USA = {
                            "PXL_FILE":r"Mega Man Legends 2 (USA) (Demo)\src\DAT\LEGEND2.BIN",
                            "PXL_OFFSET":0x226800,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

subsc2P_USA = {
                            "PXL_FILE":r"Mega Man Legends 2 (USA) (Demo)\src\DAT\LEGEND2.BIN",
                            "PXL_OFFSET":0x21b800,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

subsc3P_USA = {
                            "PXL_FILE":r"Mega Man Legends 2 (USA) (Demo)\src\DAT\LEGEND2.BIN",
                            "PXL_OFFSET":0x213000,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

subsc4P_USA = {
                            "PXL_FILE":r"Mega Man Legends 2 (USA) (Demo)\src\DAT\LEGEND2.BIN",
                            "PXL_OFFSET":0x20E000,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

#### Game Over
gover1C =          {
                            "CLUT_FILE":r"unpack\DAT\G_OVER00\G_OVER00-0x00000000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }



gover1P = {
                            "PXL_FILE":r"unpack\DAT\G_OVER00\G_OVER00-0x00000000-3.uncomp.bin",
                            "PXL_OFFSET":0x200,
                            "WIDTH":0x220,
                            "HEIGHT":0x3C,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

gover2P = {
                            "PXL_FILE":r"unpack\DAT\G_OVER00\G_OVER00-0x00002800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":0x220,
                            "HEIGHT":0x3C,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

gover3P = {
                            "PXL_FILE":r"unpack\DAT\G_OVER00\G_OVER00-0x00005800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":0x220,
                            "HEIGHT":0x3C,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

gover4P = {
                            "PXL_FILE":r"unpack\DAT\G_OVER00\G_OVER00-0x00008000-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":0x220,
                            "HEIGHT":0x1C,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

#ImageHill.convertImage(subsc4P_USA, subscC, "subsc4_USA.PNG", True)
#ImageHill.convertImage(subsc3P_USA, subscC, "subsc3_USA.PNG", True)
#ImageHill.convertImage(subsc2P_USA, subscC, "subsc2_USA.PNG", True)
#ImageHill.convertImage(subscP_USA, subscC, "subsc_USA.PNG", True)
#ImageHill.convertImage(subsc4P, subscC, "subsc4.PNG", True)
#ImageHill.convertImage(gover1P, gover1C, "gover1.PNG", True)
#ImageHill.convertImage(gover2P, gover1C, "gover2.PNG", True)
#ImageHill.convertImage(gover3P, gover1C, "gover3.PNG", True)
#ImageHill.convertImage(gover4P, gover1C, "gover4.PNG", True)


space_width = 0x3

def get_vwf(font_path, vwf_bin_path, glyph_w, glyph_h, n_rows, n_columns):
    font_im = Image.open(font_path)
    vwf_file = open(vwf_bin_path, "r+b")
    
    for j in range(n_rows):
        for i in range(n_columns):
            sub_image = font_im.crop((i*glyph_w, j*glyph_h, i*glyph_w + glyph_w, j*glyph_h + glyph_h))
            #sub_image.show()
            glyph_bbox = sub_image.getbbox()
            if not glyph_bbox:
                vwf_file.write(space_width.to_bytes(1, "little"))
                continue

            glyph_kern_width = glyph_bbox[2] - glyph_bbox[0]
            vwf_file.write(glyph_kern_width.to_bytes(1, "little"))
            
    vwf_file.close()            
    
    return

def inject_font(out_file_path):
    ImageHill.injectImage(font_pxl_inject_1, font_clut1, "font_1_edit.png")
    ImageHill.injectImage(font_pxl_inject_2, font_clut2, "font_2.PNG")

    font_path_1 = font_pxl_inject_1["PXL_FILE"]
    font_path_2 = font_pxl_inject_2["PXL_FILE"]

    buffer = b""

    pxl_start = font_pxl_inject_1["PXL_OFFSET"]

    font_file_1 = open(font_path_1, 'rb')
    font_file_2 = open(font_path_2, "rb")

    out_file = open(out_file_path, "r+b")

    out_file.seek(pxl_start)
    font_file_1.seek(pxl_start)
    font_file_2.seek(pxl_start)

    for x in range((os.stat(font_path_1).st_size - pxl_start)//4):
        word_1 = int.from_bytes(font_file_1.read(4), 'little')
        word_2 = int.from_bytes(font_file_2.read(4), 'little')

        out_word = word_1 | word_2

        out_file.write(out_word.to_bytes(4, "little"))
    return

#inject_font("unpack_edit\\DAT\\INIT\\INIT-0x00013800-2.bin")
#get_vwf("font_1.PNG", "vwf_test.bin", 12, 12, 11, 20)