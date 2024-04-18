import filesys
import MMLtext
import gfx
import subprocess
import os
import shutil

def build():
    shutil.copyfile("src\\SLPS_021.09","src_edit\\SLPS_021.09")
    MMLtext.injectAll("recieved\\MML_text.txt", "src_edit\\SLPS_021.09")
    
    gfx.inject_font("unpack_edit\\DAT\\INIT\\INIT-0x00013800-2.bin")
    gfx.get_vwf("font_1_edit.PNG", "vwf.bin", 12, 12, 13, 20)
    gfx.inject_subsc()
    gfx.inject_scene()
    
    subprocess.call(["armips.exe","SLPS_021.09.asm"])
    shutil.copy("src_edit\\SLPS_021.09", "roll_build\\SLPS_021.09")

    filesys.packDATs("roll_build\\DAT")

    

    os.remove("roll_build\\ROCKMAN.bin")
    os.remove("roll_build\\ROCKMAN.cue")

    os.chdir("roll_build")
    subprocess.call(["mkpsxiso.exe","ROCK.xml"])
    os.chdir("..")
    filesys.updateLBAs("roll_build\\SLPS_021.09")
    
    os.remove("roll_build\\ROCKMAN.bin")
    os.remove("roll_build\\ROCKMAN.cue")
    
    os.chdir("roll_build")
    subprocess.call(["mkpsxiso.exe","ROCK.xml"])
    return


#subprocess.call(["armips.exe","SLPS_021.09.asm"])
build()