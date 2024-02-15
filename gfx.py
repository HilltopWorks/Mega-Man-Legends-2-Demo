import ImageHill
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont



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

#ImageHill.convertImage(font_pxl, font_clut1, "font_1.PNG", True)
#ImageHill.convertImage(font_pxl, font_clut2, "font_2.PNG", True)

space_width = 0x4

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

    for x in range(os.stat(font_path_1).st_size//4):
        word_1 = int.from_bytes(font_file_1.read(4), 'little')
        word_2 = int.from_bytes(font_file_2.read(4), 'little')

        out_word = word_1 | word_2

        out_file.write(out_word.to_bytes(4, "little"))
    return

inject_font("unpack_edit\\DAT\\INIT\\INIT-0x00013800-2.bin")
#get_vwf("font_1.PNG", "vwf_test.bin", 12, 12, 11, 20)