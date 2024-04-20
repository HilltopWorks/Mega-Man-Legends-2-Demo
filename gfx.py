import ImageHill
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil

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


end_1_1_C_USA =          {
                            "CLUT_FILE":r"gfx\USA\LEGEND2-0x00066800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

######################################

end_1_1_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x00066800-3.uncomp.bin",
                            "PXL_OFFSET":0x200,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_2_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x00062800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":72,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_3_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x00051000-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_4_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x0007d000-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":72,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_5_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x0004c000-3.uncomp.bin",
                            "PXL_OFFSET":0x200,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_6_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x0005c000-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_7_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x00056800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_8_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x00071800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_9_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x00077800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

end_1_10_P_USA = {
                            "PXL_FILE":r"gfx\USA\LEGEND2-0x0006c000-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":320,
                            "HEIGHT":102,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

#ImageHill.gridConvert([end_1_5_P_USA, end_1_1_P_USA, end_1_3_P_USA, end_1_10_P_USA, end_1_7_P_USA, end_1_8_P_USA, end_1_6_P_USA, end_1_9_P_USA, end_1_2_P_USA, end_1_4_P_USA],
#                      [end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA,  end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA],
#                      "gfx\\USA\\grid_test.png", (2,5), show_output=True)

#ImageHill.gridInject([end_1_5_P_USA, end_1_1_P_USA, end_1_3_P_USA, end_1_10_P_USA, end_1_7_P_USA, end_1_8_P_USA, end_1_6_P_USA, end_1_9_P_USA, end_1_2_P_USA, end_1_4_P_USA],
#                      [end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA,  end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA, end_1_1_C_USA],
#                      "gfx\\USA\\grid_test.png", (2,5))
#ImageHill.convertImage(end_1_10_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_10.png", True)
#ImageHill.convertImage(end_1_9_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_9.png", True)
#ImageHill.convertImage(end_1_8_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_8.png", True)
#ImageHill.convertImage(end_1_7_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_7.png", True)
#ImageHill.convertImage(end_1_6_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_6.png", True)
#ImageHill.convertImage(end_1_5_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_5.png", True)
#ImageHill.convertImage(end_1_4_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_4.png", True)
#ImageHill.convertImage(end_1_3_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_3.png", True)
#ImageHill.convertImage(end_1_2_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_2.png", True)
#ImageHill.convertImage(end_1_1_P_USA, end_1_1_C_USA, "gfx\\USA\\end_1_1.png", True)

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


###Scene 23
S23_1C =          {
                            "CLUT_FILE":r"unpack\DAT\ST23T\ST23T-0x00043800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

S23_1P = {
                            "PXL_FILE":r"unpack\DAT\ST23T\ST23T-0x00043800-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":0x100,
                            "HEIGHT":0x100,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

S23_2P = {
                            "PXL_FILE":r"unpack\DAT\ST23T\ST23T-0x00046800-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":0x100,
                            "HEIGHT":0x100,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

S23_crateC = {
                            "CLUT_FILE":r"unpack\DAT\ST23T\ST23T-0x00041000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

S23_crateP =  {
                            "PXL_FILE":r"unpack\DAT\ST23T\ST23T-0x00041000-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":0x100,
                            "HEIGHT":0x100,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
S25_crateP =  {
                            "PXL_FILE":r"unpack\DAT\ST25T\ST25T-0x00049000-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":0x100,
                            "HEIGHT":0x100,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }


###Scene 25
S25_1C =          {
                            "CLUT_FILE":r"unpack\DAT\ST25T\ST25T-0x0004d800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

S25_1P = {
                            "PXL_FILE":r"unpack\DAT\ST25T\ST25T-0x0004d800-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":0x100,
                            "HEIGHT":0x100,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }


#BOOT

disclaimerC =  {
                            "CLUT_FILE":r"unpack\DAT\LOGO\LOGO-0x00002000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

disclaimerP = {
                            "PXL_FILE":r"unpack\DAT\LOGO\LOGO-0x00002000-3.uncomp.bin",
                            "PXL_OFFSET":0x20,
                            "WIDTH":640,
                            "HEIGHT":64,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }



main_menuC_1 =  {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

main_menuC_2 =  {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

main_menuC_3 =  {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0x40,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

main_menuC_4 =  {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0x60,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

main_menuC_5 =  {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0x80,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

main_menuC_6 =  {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0xa0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

main_menuP = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_INSET":0,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

main_menuP_1 = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0,
                            "WIDTH":208,
                            "HEIGHT":38,
                            "PXL_INSET":24,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

main_menuP_2 = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0 + 128*41,
                            "WIDTH":208,
                            "HEIGHT":38,
                            "PXL_INSET":24,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

main_menuP_3 = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0 + 128*83,
                            "WIDTH":208,
                            "HEIGHT":33,
                            "PXL_INSET":24,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

main_menuP_4 = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0 + 128*124,
                            "WIDTH":208,
                            "HEIGHT":32,
                            "PXL_INSET":24,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

main_menuP_5 = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0 + 128*37 + 104,
                            "WIDTH":48,
                            "HEIGHT":91,
                            "PXL_INSET":104,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

main_menuP_6 = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xc0 + 128*160,
                            "WIDTH":232,
                            "HEIGHT":32,
                            "PXL_INSET":12,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

#### SELECT


selectC_1 =  {
                            "CLUT_FILE":r"unpack\DAT\SELECT\SELECT-0x00004800-3.uncomp.bin",
                            "CLUT_OFFSET":0x0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

selectC_2 =  {
                            "CLUT_FILE":r"unpack\DAT\SELECT\SELECT-0x0001c800-3.uncomp.bin",
                            "CLUT_OFFSET":0x0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }


selectP_1 = {
                            "PXL_FILE":r"unpack\DAT\SELECT\SELECT-0x00000000-3.uncomp.bin",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_INSET":0,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

selectP_2 = {
                            "PXL_FILE":r"unpack\DAT\SELECT\SELECT-0x00004800-3.uncomp.bin",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_INSET":0,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

selectP_3 = {
                            "PXL_FILE":r"unpack\DAT\SELECT\SELECT-0x0001c800-3.uncomp.bin",
                            "PXL_OFFSET":0x200,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_INSET":0,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

selectP_4 = {
                            "PXL_FILE":r"unpack\DAT\SELECT\SELECT-0x00020800-3.uncomp.bin",
                            "PXL_OFFSET":0x0,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_INSET":0,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }

#### Game Over
tron_1C =          {
                            "CLUT_FILE":r"unpack\DAT\TITLE\TITLE-0x00013000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

tron_1P = {
                            "PXL_FILE":r"unpack\DAT\TITLE\TITLE-0x00013000-3.uncomp.bin",
                            "PXL_OFFSET":0x100,
                            "WIDTH":0x100,
                            "HEIGHT":0x100,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

def inject_subsc():
    image_edits = ["gfx\\subsc1.png", "gfx\\subsc2.png", "gfx\\subsc3.png", "gfx\\subsc4.png" ]
    images = [subsc1P, subsc2P, subsc3P, subsc4P]
    for image_index in range(len(images)):
        
        images[image_index]["PXL_FILE"] = images[image_index]["PXL_FILE"].replace("unpack", "unpack_edit")
        ImageHill.injectImage(images[image_index], subscC, image_edits[image_index])

    return

def inject_scene():
    image_edits = ["gfx\\S23_1_edit.png", "gfx\\S23_2_edit.png", "gfx\\S25_1_edit.png", "gfx\\S23_crate_edit.png", "gfx\\S23_crate_edit.png", "gfx\\disclaimer_edit.png" ]
    images = [S23_1P, S23_2P, S25_1P, S23_crateP, S25_crateP, disclaimerP]
    cluts  = [S23_1C, S23_1C, S25_1C, S23_crateC, S23_crateC, disclaimerC]
    for image_index in range(len(images)):
        images[image_index]["PXL_FILE"] = images[image_index]["PXL_FILE"].replace("unpack", "unpack_edit")
        ImageHill.injectImage(images[image_index], cluts[image_index], image_edits[image_index])

    return

def inject_select():
    shutil.copy(r"gfx\USA\LEGEND2-0x004e2000-3.uncomp.bin", r"unpack_edit\DAT\SELECT\SELECT-0x0001c800-3.uncomp.bin")
    shutil.copy(r"gfx\USA\LEGEND2-0x004e4800-3.uncomp.bin", r"unpack_edit\DAT\SELECT\SELECT-0x00020800-3.uncomp.bin")
    return

#ImageHill.convertImage(selectP_4, selectC_2, "gfx\\select_4.png", True)
#ImageHill.convertImage(selectP_3, selectC_2, "gfx\\select_3.png", True)
#ImageHill.convertImage(selectP_2, selectC_1, "gfx\\select_2.png", True)
#ImageHill.convertImage(selectP_1, selectC_1, "gfx\\select_1.png", True)
#ImageHill.convertImage(main_menuP_6, main_menuC_2, "gfx\\main_menu_6.png", True)
#ImageHill.convertImage(main_menuP_5, main_menuC_5, "gfx\\main_menu_5.png", True)
#ImageHill.convertImage(subsc4P_USA, subscC, "subsc4_USA.PNG", True)
#ImageHill.convertImage(subsc3P_USA, subscC, "subsc3_USA.PNG", True)
#ImageHill.convertImage(subsc2P_USA, subscC, "subsc2_USA.PNG", True)
#ImageHill.convertImage(subscP_USA, subscC, "subsc_USA.PNG", True)
#ImageHill.convertImage(subsc4P, subscC, "subsc4.PNG", True)
#ImageHill.convertImage(gover1P, gover1C, "gover1.PNG", True)
#ImageHill.convertImage(gover2P, gover1C, "gover2.PNG", True)
#ImageHill.convertImage(gover3P, gover1C, "gover3.PNG", True)
#ImageHill.convertImage(gover4P, gover1C, "gover4.PNG", True)
#ImageHill.convertImage(S23_1P, S23_1C, "S23_1.PNG", True)
#ImageHill.convertImage(S23_2P, S23_1C, "S23_2.PNG", True)
#ImageHill.convertImage(S25_1P, S25_1C, "S25_1.PNG", True)
#ImageHill.convertImage(S23_crateP, S23_crateC, "gfx\\S23_crate.PNG", True)
#ImageHill.convertImage(disclaimerP, disclaimerC, "gfx\\disclaimer.PNG", True)
#ImageHill.convertImage(tron_1P, tron_1C, "tron.PNG", True)

space_width = 0x5

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