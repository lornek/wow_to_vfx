import os
import sys
import subprocess
import glob
import argparse
import fnmatch
import hou

obj     = hou.node("/obj")
shop    = hou.node("/shop")
hda     = "wow_asset_loader"
shad    = "uber_rs"

def genProxy(file):
    # Create WoW Loader HDA
    loader = obj.createNode(hda, "loader")
    loader.parm("file").set(file)
    loader.node("file").cook(force=True)
    loader.parm("eval_py").pressButton()
    for child in loader.node("instancer").children():
        child.updateParmStates()
        child.cook(force=True)
    csv_out = loader.node("instancer/output1")
    num_csv = csv_out.geometry().intrinsicValue("pointcount")
    loader.parm("execute").pressButton()
    hou.Node.destroy(loader)
    for child in shop.children():
        hou.Node.destroy(child)
    return None
    
def loopAllFiles(folder_path, start = 0, inc = 1):
    if not os.path.isdir(folder_path):
        raise ValueError("Input must be a folder")
    objs = glob.glob1(folder_path, '*.obj')[start::inc]
    num_objs = len(objs)
    print "Generating .rs proxy files for " + str(num_objs) + " objects in this directory"
    for idx, item in enumerate(objs, start=0):
        full_path = "/".join([folder_path, item])
        folder_name = os.path.basename(folder_path)
        item_split = item.split("_")[0]
        # Skip any objects that are terrain based on their name starting with the same string as the root folder
        if (item_split == folder_name):
            print("Terrain object detected. Skipping.")
            return None
        genProxy(full_path)
        print str(round(float(idx)/float(num_objs)*100, 2)) + "% Complete"
        print "_______________________________________________"
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start WoW asset .rs proxy generation ")
    parser.add_argument("folder", help="Folder path", type=str)
    parser.add_argument("-start", help="Start index", type=int, default="0")
    parser.add_argument("-inc", help="Increment", type=int, default="1")
    args = parser.parse_args()

loopAllFiles(args.folder, args.start, args.inc)