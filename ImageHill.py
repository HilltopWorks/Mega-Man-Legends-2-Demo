import sys    
import os
import math
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
import TIMresource

#CLUT MODES
NO_CLUT = -1
RGB_555 = 0
RGBA_32_PS2 = 1  #0-128 alpha
RGBA_32 = 2      #0-128 alpha no PS2 swizzle
RGBA_5551_PS1 = 3
BITMAP_RGBX = 4

    #PXL MODES
#Indexed
ONE_BIT = 0
TWO_BIT = 1
FOUR_BIT = 2
EIGHT_BIT = 3
#Direct color
FIFTEEN_BIT_DIRECT = 4
TWENTY_FOUR_BIT_DIRECT = 5
THIRTY_TWO_BIT_DIRECT = 6
SIXTEEN_BIT_PS1_DIRECT = 7
THIRTY_TWO_BIT_PS2_DIRECT = 8

#Flip Modes
NO_FLIP = -1
HORIZONTAL = 0
VERTICAL = 1
HORIZONTAL_AND_VERTICAL = 2

def readPXL(file, offset, width, height, mode, inset=-1):
    file.seek(offset)
    buffer = []
    if mode == EIGHT_BIT:
        #buffer = list(file.read(width*height))
        for y in range(height):
            buffer += list(file.read(width))
            
            if inset != -1:
                file.read(inset) #Skip inset bytes if horizontally stacked image
                
    elif mode == FOUR_BIT:
        for y in range(height):
            for x in range(width//2):
                next_byte = int.from_bytes(file.read(1), "little")
                buffer.append(next_byte&0b1111)
                buffer.append((next_byte&0b11110000)>>4)
            if inset != -1:
                file.read(inset) #Skip inset bytes if horizontally stacked image
    elif mode == SIXTEEN_BIT_PS1_DIRECT or mode == FIFTEEN_BIT_DIRECT:
        for y in range(height):
            for x in range(width):
                buffer.append(int.from_bytes(file.read(2), "little"))
            if inset != -1:
                file.read(inset) #Skip inset bytes if horizontally stacked image
                
    elif mode == TWENTY_FOUR_BIT_DIRECT:
        for y in range(height):
            for x in range(width):
                buffer.append(int.from_bytes(file.read(3), "little"))
            if inset != -1:
                file.read(inset) #Skip inset bytes if horizontally stacked image
    elif mode == THIRTY_TWO_BIT_PS2_DIRECT:
        for y in range(height):
            for x in range(width):
                buffer.append(int.from_bytes(file.read(4), "little"))
            if inset != -1:
                file.read(inset) #Skip inset bytes if horizontally stacked image
    return buffer

def getColorCount(mode):
    
    if mode == 0:
        count = 2
    elif mode == 1:
        count = 4
    elif mode == 2:
        count = 16
    elif mode == 3:
        count = 256
    else:
        count = 0
        '''
    match mode:
        case 0:#one bit
            count = 2
        case 1:#two bit
            count = 4
        case 2:#four bit
            count = 16
        case 3:#eight bit
            count = 256
        case _:#no clut or unidentified
            count = 0'''

    return count

def changeBase(num, old_base, new_base):
    fraction = num/old_base
    value = math.floor(fraction*new_base)
    return value

def readCLUT(file, offset, n_entries, mode):
    
    buffer = []
    
    if mode == BITMAP_RGBX:
        file.seek(offset)
        for x in range(n_entries):
            entry_value = int.from_bytes(file.read(4), "little")
            blue  = (entry_value & 0x000000FF)
            green = (entry_value & 0x0000FF00) >> 8
            red   = (entry_value & 0x00FF0000) >> 16
            alpha = 255
            buffer.append((red,green,blue,alpha))
    elif mode == RGBA_5551_PS1:
        file.seek(offset)
        for x in range(n_entries):
            entry_value = int.from_bytes(file.read(2), "little")
            red   = (entry_value & 0b11111) << 3
            #red = changeBase(red, 31, 255)
            green = (entry_value & 0b1111100000) >> 2
            #green = changeBase(green, 31, 255)
            blue  = (entry_value & 0b111110000000000) >> 7
            #blue = changeBase(blue, 31, 255)
            STP =   (entry_value & 0b1000000000000000) >> 15
            if red == green == blue == STP == 0:
                alpha = 0
            else:
                alpha = 255
            
            buffer.append((red,green,blue,alpha))
    elif mode == RGBA_32_PS2:
        file.seek(offset)
        if n_entries > 16:
            for x in range(n_entries//8):
                #Swizzle
                block_number = x % 4
                if block_number == 0:
                    pass
                elif block_number == 1:
                    file.seek(file.tell() + 4*8)
                elif block_number == 2:
                    file.seek(file.tell() - 4*8*2)
                elif block_number == 3:
                    file.seek(file.tell() + 4*8)
                    
                for y in range(8):
                    entry_value = int.from_bytes(file.read(4), "little")
                    red =    entry_value & 0xFF
                    green = (entry_value & 0xFF00)>>8
                    blue =  (entry_value & 0xFF0000)>>16
                    alpha = (entry_value & 0xFF000000)>>24
                    buffer.append((red, green, blue, min(255, alpha*2)))
        else:
            for x in range(n_entries):
                entry_value = int.from_bytes(file.read(4), "little")
                red =    entry_value & 0xFF
                green = (entry_value & 0xFF00)>>8
                blue =  (entry_value & 0xFF0000)>>16
                alpha = (entry_value & 0xFF000000)>>24
                buffer.append((red, green, blue, min(255, alpha*2)))
    elif mode == RGBA_32:
        file.seek(offset)
        for x in range(n_entries):
            entry_value = int.from_bytes(file.read(4), "little")
            red  = (entry_value & 0x000000FF)
            green = (entry_value & 0x0000FF00) >> 8
            blue   = (entry_value & 0x00FF0000) >> 16
            alpha = (entry_value & 0xFF000000)>>24
            buffer.append((red, green, blue, min(255, alpha*2)))
        
    elif mode == NO_CLUT:
        buffer = []
    return buffer


def convertDirectColor(pxl, width, height, color_mode, flip_mode = NO_FLIP):
    
    im = Image.new("RGBA", (width,height), (0, 0, 0, 0))
    
    if color_mode == SIXTEEN_BIT_PS1_DIRECT:
        for y in range(height):
            for x in range(width):
                val = pxl[width*y + x]
                red = val & 0b11111
                green = (val & 0b1111100000) >> 5
                blue = (val & 0b111110000000000) >> 10
                semitransparency_flag = (val & 0x8000)
                
                if red == green == blue == semitransparency_flag == 0:
                    pixel =  (red<<3, green<<3, blue<<3, 0)
                else:
                    pixel =  (red<<3, green<<3, blue<<3, 255)

                im.putpixel((x,y), pixel)
    elif color_mode == THIRTY_TWO_BIT_PS2_DIRECT or color_mode == THIRTY_TWO_BIT_DIRECT:
        for y in range(height):
            for x in range(width):
                val = pxl[width*y + x]
                red    = val & 0xFF
                green = (val & 0xFF00) >> 8
                blue =  (val & 0xFF0000) >> 16
                alpha = (val & 0xFF000000) >> 24
                
                if color_mode == THIRTY_TWO_BIT_DIRECT:
                    pixel = (red, green, blue, alpha)
                elif color_mode == TWENTY_FOUR_BIT_DIRECT:
                    pixel = (red, green, blue, 255)
                else:
                    pixel = (red, green, blue, min(alpha*2, 255))
                
                im.putpixel((x,y), pixel)
    
    
    return im

def getBMP(path, offset):
    file = open(path, 'rb')
    file.seek(0xA)
    pxl_offset = int.from_bytes(file.read(4), "little") + offset
    clut_offset = int.from_bytes(file.read(4), "little") + 0xE + offset

    width  = int.from_bytes(file.read(4), "little")
    height = int.from_bytes(file.read(4), "little")
    
    planes          = int.from_bytes(file.read(2), "little")
    pixel_bit_count = int.from_bytes(file.read(2), "little")
    compression = int.from_bytes(file.read(4), "little")
    
    file.seek(0x2E)
    color_count = int.from_bytes(file.read(4), "little")
    
    clut = {}
    if color_count == 0:
        clut["CLUT_MODE"] = NO_CLUT
    else:
        clut["CLUT_OFFSET"] = clut_offset
        clut["CLUT_FILE"] = path
        clut["CLUT_MODE"] = BITMAP_RGBX
        clut["N_COLORS"] = color_count
    pxl = {}
    pxl["PXL_FILE"] = path
    pxl["PXL_OFFSET"] = pxl_offset
    pxl["FLIP"] = VERTICAL
    
    pxl["HEIGHT"] = height
    pxl["WIDTH"] = width
    if pixel_bit_count == 8:
        pxl["PXL_MODE"] = EIGHT_BIT
    elif pixel_bit_count == 4:
        pxl["PXL_MODE"] = FOUR_BIT
    elif pixel_bit_count == 24:
        pxl["PXL_MODE"] = TWENTY_FOUR_BIT_DIRECT
    return pxl, clut

def getTIM(path, offset, STP_mode=TIMresource.STP_FIFTY_FIFTY):
    file = open(path, 'rb')
    file.read(offset)
    timObj = TIMresource.TIM(file)
    
    if timObj.CF==1:
        cluts = []
        total_colors = (timObj.CLUT.bnum - 0xC)//2
        if timObj.PMD == TIMresource.FOUR_BIT_CLUT:
            palette_colors =  16
        elif timObj.PMD == TIMresource.EIGHT_BIT_CLUT:
            palette_colors =  256
        
        n_cluts = total_colors//palette_colors
        
        for n in range(n_cluts):
            clut = {}
            clut["CLUT_OFFSET"] = timObj.CLUT_offset
            clut["CLUT_FILE"] = path
            clut["CLUT_MODE"] = RGBA_5551_PS1
            if timObj.PMD == TIMresource.FOUR_BIT_CLUT:
                clut["N_COLORS"] = 16
            elif timObj.PMD == TIMresource.EIGHT_BIT_CLUT:
                clut["N_COLORS"] = 256
            else:
                assert False, "Bad PMD mode: " + path
                
            cluts.append(clut)
    
    pxl = {}
    
    pxl["PXL_FILE"] = path
    pxl["PXL_OFFSET"] = timObj.PXL_offset
    pxl["HEIGHT"] = timObj.H
    if timObj.PMD == TIMresource.FOUR_BIT_CLUT:
        pxl["WIDTH"] = timObj.W*4
        pxl["PXL_MODE"] = FOUR_BIT
        
    elif  timObj.PMD == TIMresource.EIGHT_BIT_CLUT:
        pxl["WIDTH"] = timObj.W*2
        pxl["PXL_MODE"] = EIGHT_BIT
    elif timObj.PMD == TIMresource.SIXTEEN_BIT_CLUT:
        pxl["WIDTH"] = timObj.W
        pxl["PXL_MODE"] = SIXTEEN_BIT_PS1_DIRECT
        clut = {"CLUT_MODE":NO_CLUT}
        return pxl, [clut]
    
    return pxl, cluts

def extractTIM(path, offset, outfolder, STP_mode=TIMresource.STP_FIFTY_FIFTY):
    pxl, cluts = getTIM(path, offset)
    
    file_stem = Path(path).stem
    
    for clut_number in range(len(cluts)):
        out_path = os.path.join(outfolder, file_stem + "-offset-" + hex(offset) + "-CLUT-" + hex(clut_number) + ".PNG")
        convertImage(pxl, cluts[clut_number], out_path)
        
    return

def injectTIM(path, offset, PNG_path, clut_number = 0):
    pxl, cluts =  getTIM(path, offset)
    injectImage(pxl, cluts[clut_number], PNG_path)
    return

def convertImage(image_definition, clut_definition, output_path, show_output=False, STP_MODE=TIMresource.STP_OFF):
    image_file = open(image_definition["PXL_FILE"], "rb")
    
    if "PXL_INSET" in image_definition:
        inset = image_definition["PXL_INSET"]
    else:
        inset = -1
    pxl = readPXL(image_file, image_definition["PXL_OFFSET"], image_definition["WIDTH"],image_definition["HEIGHT"], image_definition["PXL_MODE"], inset)
    
    height = image_definition["HEIGHT"]
    width = image_definition["WIDTH"]
    
    if clut_definition["CLUT_MODE"] != NO_CLUT:
        #indexed color
        clut_file = open(clut_definition["CLUT_FILE"], "rb")
        n_clut_entries = getColorCount(image_definition["PXL_MODE"])
        clut = readCLUT(clut_file,clut_definition["CLUT_OFFSET"], n_clut_entries, clut_definition["CLUT_MODE"])
        
        im = Image.new("RGBA", (image_definition["WIDTH"],image_definition["HEIGHT"]), (0, 0, 0, 0))

        for y in range(height):
            for x in range(width):
                pixel =  clut[pxl[y*image_definition["WIDTH"] + x]]  
                im.putpixel((x,y), pixel)
        if "FLIP" in image_definition:
            if image_definition["FLIP"] == HORIZONTAL:
                im = ImageOps.mirror(im)
            elif image_definition["FLIP"] == VERTICAL:
                im = ImageOps.flip(im)
            elif image_definition["FLIP"] == HORIZONTAL_AND_VERTICAL:
                im = ImageOps.mirror(im)
                im = ImageOps.flip(im)
        if show_output:
            im.show()
        im.save(output_path)
    else:
        #direct color
        im = convertDirectColor(pxl, image_definition["WIDTH"],image_definition["HEIGHT"], image_definition["PXL_MODE"], flip_mode = NO_FLIP)
        
        if "FLIP" in image_definition:
            if image_definition["FLIP"] == HORIZONTAL:
                im = ImageOps.mirror(im)
            elif image_definition["FLIP"] == VERTICAL:
                im = ImageOps.flip(im)
            elif image_definition["FLIP"] == HORIZONTAL_AND_VERTICAL:
                im = ImageOps.mirror(im)
                im = ImageOps.flip(im)
        if show_output:
            im.show()
        im.save(output_path)
    return im

def gridConvert(images, cluts, output_path, dimensions, show_output=False, STP_MODE = TIMresource.STP_OFF):

    assert len(images) == len(cluts) and len(images) == dimensions[0]*dimensions[1], "GRID DIMENSIONS DO NOT MATCH IMAGES PASSED TO GRIDCONVERT"

    output_extension = Path(output_path).suffix
    for image_number in range(len(images)):
        convertImage(images[image_number], cluts[image_number], output_path.replace(output_extension, "_" + str(image_number).zfill(2) + output_extension))

    width_total = 0
    height_total = 0
    for i in range(dimensions[0]):
        cell_width = images[i*dimensions[1]]["WIDTH"]
        width_total += cell_width
    for j in range(dimensions[1]):
        cell_height = images[j*dimensions[0]]["HEIGHT"]
        height_total += cell_height
    
    canvas = Image.new("RGBA", (width_total, height_total), (0,0,0,0))

    x_cursor = 0
    y_cursor = 0
    for j in range(dimensions[1]):
        for i in range(dimensions[0]):
            image_number = i + j*dimensions[0]
            cell_image = Image.open(output_path.replace(output_extension, "_" + str(image_number).zfill(2) + output_extension))
            canvas.paste(cell_image, (x_cursor, y_cursor))
            x_cursor += cell_image.width
        x_cursor = 0
        y_cursor += cell_image.height
    
    if show_output:
        canvas.show()
    canvas.save(output_path)
    return

def closest(color,colors, color_dict):
    if color in color_dict:
        return color_dict[color]
    
    if color[3] == 0:
        return getAlpha(colors)
    #colors = np.array(colors)
    color_array = np.array(color)
    
    distances = np.sqrt(np.sum((colors-color_array)**2,axis=1))
    index_of_smallest = int(np.where(distances==np.amin(distances))[0][0])
    #smallest_distance = colors[index_of_smallest]
    color_dict[color] = index_of_smallest
    return index_of_smallest

def getAlpha(palette):
    for color_num in range(len(palette)):
        if palette[color_num][3] == 0:
            return color_num

    #print("ERROR: ALPHA NOT FOUND!!!!")
    return 0

def gridInject(images, cluts, png_path, dimensions, STP_mode=TIMresource.STP_OFF):

    canvas = Image.open(png_path)
    x_cursor = 0
    y_cursor = 0
    for j in range(dimensions[1]):
        for i in range(dimensions[0]):
            image_number = i + j*dimensions[0]
            cell_image = canvas.crop((x_cursor, y_cursor, x_cursor + images[image_number]["WIDTH"], y_cursor + images[image_number]["HEIGHT"]))
            cell_image_path = png_path.replace(".png", "_" + str(image_number).zfill(2) + ".png")
            cell_image.save(cell_image_path)

            injectImage(images[image_number], cluts[image_number], cell_image_path, STP_mode)
            x_cursor += cell_image.width
        x_cursor = 0
        y_cursor += cell_image.height

    return

def injectImage(imagedef, clutdef, png_path, STP_mode=TIMresource.STP_OFF):
    print("Injecting PXL:", imagedef, "\nCLUT:", clutdef, "\nPNG:", png_path,"\n")
    #Open and read clut
    if clutdef["CLUT_MODE"] != NO_CLUT:
        clut_parent_path = clutdef["CLUT_FILE"]
        clut_parent_file = open(clut_parent_path, "rb")
        clut = readCLUT(clut_parent_file, clutdef["CLUT_OFFSET"], clutdef["N_COLORS"], clutdef["CLUT_MODE"])
        clut = np.array(clut)
        pass
    
    #Open pxl
    pxl_parent_path = imagedef["PXL_FILE"]
    pxl_parent_file = open(pxl_parent_path, "r+b")
    pxl_parent_file.seek(imagedef["PXL_OFFSET"])
    
    edited_im = Image.open(png_path).convert("RGBA")
    
    color_dict = {}
    
    if "FLIP" in imagedef:
        if imagedef["FLIP"] == HORIZONTAL:
            edited_im = ImageOps.mirror(edited_im)
        elif imagedef["FLIP"] == VERTICAL:
            edited_im = ImageOps.flip(edited_im)
        elif imagedef["FLIP"] == HORIZONTAL_AND_VERTICAL:
            edited_im = ImageOps.mirror(edited_im)
            edited_im = ImageOps.flip(edited_im)
    
    pxl_mode = imagedef["PXL_MODE"]
    if pxl_mode == ONE_BIT:
        #TODO
        pass
    elif pxl_mode == TWO_BIT:
        for y in range(imagedef["HEIGHT"]):
            for x in range(imagedef["WIDTH"]//4):
                x1 = x*4
                y1 = y
                edit_color1 = edited_im.getpixel((x1, y1))
                val1 = closest(edit_color1, clut, color_dict)
                
                x2 = x*4 + 1
                y2 = y
                edit_color2 = edited_im.getpixel((x2, y2))
                val2 = closest(edit_color2, clut, color_dict)
                
                x3 = x*4 + 2
                y3 = y
                edit_color3 = edited_im.getpixel((x3, y3))
                val3 = closest(edit_color3, clut, color_dict)
                
                x4 = x*4 + 3
                y4 = y
                edit_color4 = edited_im.getpixel((x4, y4))
                val4 = closest(edit_color4, clut, color_dict)
                
                new_byte = val1 | (val2 << 2) | (val3 << 4) | (val4 << 6)
                pxl_parent_file.write(new_byte.to_bytes(1, "little"))
            
            if "PXL_INSET" in imagedef:
                pxl_parent_file.read(imagedef["PXL_INSET"])
    elif pxl_mode == FOUR_BIT:
        for y in range(imagedef["HEIGHT"]):
            for x in range(imagedef["WIDTH"]//2):
                x1 = x*2
                y1 = y
                edit_color1 = edited_im.getpixel((x1, y1))
                val1 = closest(edit_color1, clut, color_dict)
                
                x2 = x*2 + 1
                y2 = y
                edit_color2 = edited_im.getpixel((x2, y2))
                val2 = closest(edit_color2, clut, color_dict)
                new_byte = val1 | (val2 << 4)
                pxl_parent_file.write(new_byte.to_bytes(1, "little"))
            
            if "PXL_INSET" in imagedef:
                pxl_parent_file.read(imagedef["PXL_INSET"])
    elif pxl_mode == EIGHT_BIT:
        for y in range(imagedef["HEIGHT"]):
            for x in range(imagedef["WIDTH"]):
                edit_color = edited_im.getpixel((x, y))
                val = closest(edit_color, clut, color_dict)
                pxl_parent_file.write(val.to_bytes(1, "little"))
                
            if "PXL_INSET" in imagedef:
                pxl_parent_file.read(imagedef["PXL_INSET"])
    elif pxl_mode == SIXTEEN_BIT_PS1_DIRECT:
        for y in range(imagedef["HEIGHT"]):
            for x in range(imagedef["WIDTH"]):
                color = edited_im.getpixel((x, y))
                red = color[0]>>3
                green = color[1] >> 3
                blue = color[2] >> 3
                alpha = color[3]
                if alpha == red == green == blue == 0:
                    stp = 0
                else:
                    stp = 1
                    
                val = red | (green <<5) | (blue << 10) | (stp << 15) #R,G,B
                pxl_parent_file.write(val.to_bytes(2, "little"))
                
            if "PXL_INSET" in imagedef:
                pxl_parent_file.read(imagedef["PXL_INSET"])
    elif pxl_mode == THIRTY_TWO_BIT_PS2_DIRECT:
        for y in range(imagedef["HEIGHT"]):
            for x in range(imagedef["WIDTH"]):
                color = edited_im.getpixel((x, y))
                #red = color[0]
                #green = color[1]
                #blue = color[2]
                alpha = (color[3] + 1) //2
                
                pxl_parent_file.write(color[0].to_bytes(1, "little"))
                pxl_parent_file.write(color[1].to_bytes(1, "little"))
                pxl_parent_file.write(color[2].to_bytes(1, "little"))
                pxl_parent_file.write(alpha.to_bytes(1, "little"))
                
            if "PXL_INSET" in imagedef:
                pxl_parent_file.read(imagedef["PXL_INSET"])
    elif pxl_mode == TWENTY_FOUR_BIT_DIRECT:
        for y in range(imagedef["HEIGHT"]):
            for x in range(imagedef["WIDTH"]):
                color = edited_im.getpixel((x, y))
                #red = color[0]
                #green = color[1]
                #blue = color[2]
                
                pxl_parent_file.write(color[0].to_bytes(1, "little"))
                pxl_parent_file.write(color[1].to_bytes(1, "little"))
                pxl_parent_file.write(color[2].to_bytes(1, "little"))
    return