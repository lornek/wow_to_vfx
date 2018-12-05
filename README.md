# wow_to_vfx
Collection of Python code and Houdini tools dedicated to importing WoW game exports into Houdini

# Requirements
Houdini 17.0.352+
(www.sidefx.com)
RedShift for Houdini 17 (Support for Arnold and RenderMan might get added at some point)
(www.redshift3d.com)
Python 2.7+
(www.python.com)
Marlamin's WoW OBJ Exporter
(https://marlam.in/obj)

# Installation
  # wow_asset_loader.hda
  Copy to your prefered Houdini otl folder. Default would typically be: $HOME/houdini17.0/otls
  # wow_converter.py
  Copy to any location on your system.
  
# Tutorials
  # Houdini WoW Asset Loader
  Tab in a WoW Asset Loader in the /obj/ context
  In the file parameter, plug in the path to an .obj file exported from Marlamin's tool.
  Press the "Run Py" button and it will create shaders for every material called for by the .obj
  You can find these materials in /shop/ if you want to customize them
  Now that the shaders are made, press the "Render" button.
  A RedShift Proxy will be saved out with the same name as your original asset, but .rs instead of .obj
  This RS Proxy contains all of the shaders and any instances attached to your mesh if a .csv file was found with the same .obj basename
  That's it!
  
  # WoW Batch Asset Conversion
  This script runs in a Houdini Command Line session, it loops through every .obj file in the folder you specify and does a few things:
  1) Creates a WoW Asset Loader HDA for each .obj
  2) Generates the shaders that it needs and assigns them
  3) Saves out the .obj as a .rs Proxy
  4) Deletes all nodes that were created in the process, and moves onto the next .obj in the dir
  It also lets you set it up to start on (for example) the 2nd .obj found in the folder and do every 8th .obj
  At some point I will add a more seamless multithreading approach, but for now that's how you do it
  
  Let's convert a folder!
  I've exported the kultiras zone from Marlamin's tool to a folder on my machine -- "E:/Projects/WoW/world/maps/kultiras"
  I've saved the wow_converter.py as well -- "S:/Pipeline/cmd/wow_converter.py"
  Now I need to convert all of the .obj and .csv files in this folder into .rs proxies that will attach to the master map layout
  Open up a Houdini command shell, aka Command Line Tools 17.0.352
  We'll need to passs Houdini a command that will launch it in python mode, link to the wow_converter.py script, and give it args:
    hython "S:/Pipeline/cmd/wow_converter.py" "E:/Projects/WoW/world/maps/kultiras"
  Hit enter and this will start running
  It will tell you how many .objs are being converted, print out the shaders being created, and give you a completion percentage
  However...this conversion is taking a really long time going one by one through the 2,500 .obj files in this folder
  We can split the job up into multiple Command Line Tools windows. Launch 4 of them separately.
  In the first window, enter this:
    hython "S:/Pipeline/cmd/wow_converter.py" "E:/Projects/WoW/world/maps/kultiras" -start 0 -inc 4
  In the next window:
    hython "S:/Pipeline/cmd/wow_converter.py" "E:/Projects/WoW/world/maps/kultiras" -start 1 -inc 4
  And so on...the other two windows will get -start 2 and -start 3.
  Now we have 4 separate Houdini batches running and the progress will be roughly 4x faster.
  
  

