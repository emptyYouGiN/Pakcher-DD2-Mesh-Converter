PAKCHER - DD2 Mesh Converter
=========================================
Author: emptyYouGiN
Version: 1.1

DESCRIPTION
-----------
This tool would not exist without the groundbreaking work of DPAvg and Feuleur. Their dedication helped me cross the threshold of modding and build this instrument. Infinite kudos to them.

Pakcher is a "one-click(or not:)" utility designed to update Dragon's Dogma 2 mesh files. 
It converts old Legacy Meshes (ID 231011879) into the modern format (ID 240423143) compatible with the latest game versions.

It automates the Blender process, so you don't need to know how to 3D model.

REQUIREMENTS
------------
1. Blender 5.0 or higher (Installed via Steam or Official Website).
2. DD2 Tool Suite Addons (Included in the "Addons" folder).
3. Python 3.10+ (Latest version recommended).

INSTALLATION & SETUP
--------------------
1. Install Blender 5.0+ if you haven't already.
2. Open Blender.
3. Go to Edit -> Preferences -> Add-ons.
4. Install/Enable the addons provided in the "Addons" folder included with this download.
   (Make sure both the "Main Suite" and "Legacy Tools" are active).
5. Close Blender.

HOW TO USE
----------
Step 1: Extract your .pak
Go to the bin folder.

Drag your mod .pak file onto Extract-PAK.

Wait for the unpacking to finish.

Step 2: Convert (Pakcher)

Run Pakcher.exe.

Click Add Files and select the mesh files from the folder you just unpacked (look for files ending in .mesh.231011879).

Click CONVERT.

Pakcher will update the files and remove the old legacy versions safely.

Step 3: Repack

Go back to the bin folder.

Drag your modified folder onto Create-PAK-2024.

Install the resulting .pak into your Mods folder with Fluffy mods
---------------
- "Legacy operator not found": Ensure you have installed the addons in Blender correctly.

- "Not a mesh file": You are trying to convert a .pak archive. Unpack it first.
