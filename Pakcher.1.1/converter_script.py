import bpy
import os
import sys
import addon_utils

# --- CONFIG ---
LEGACY_ID = 231011879
NEW_ID_SUFFIX = "240423143"
LEGACY_ADDON_NAME = "dd2_legacy_tools" 

def force_enable_addons():
    # 1. Enable Legacy Addon
    try:
        if LEGACY_ADDON_NAME not in addon_utils.addons_fake_modules:
            addon_utils.enable(LEGACY_ADDON_NAME, default_set=True)
            print(f">>> FORCE ENABLED: {LEGACY_ADDON_NAME}")
    except Exception as e:
        print(f"!!! WARNING: Could not enable '{LEGACY_ADDON_NAME}'. Error: {e}")

    # 2. Enable Main Tool Suite
    try:
        for mod in addon_utils.modules():
            if "DD2 tool suite" in mod.bl_info.get("name", "") and "Legacy" not in mod.bl_info.get("name", ""):
                addon_utils.enable(mod.__name__, default_set=True)
                print(f">>> FORCE ENABLED MAIN ADDON: {mod.__name__}")
    except:
        pass

def convert_file(filepath):
    if not os.path.exists(filepath):
        return

    # Determine new filename
    if str(LEGACY_ID) in filepath:
        output_path = filepath.replace(str(LEGACY_ID), NEW_ID_SUFFIX)
    else:
        output_path = filepath + "." + NEW_ID_SUFFIX

    print(f"--- PROCESSING: {os.path.basename(filepath)} ---")
    
    # Clean Scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import
    try:
        if hasattr(bpy.ops.dd2_legacy, "import_mesh"):
            bpy.ops.dd2_legacy.import_mesh(filepath=filepath)
        else:
            print("!!! CRITICAL: Legacy operator not found!")
            return
    except Exception as e:
        print(f"!!! Import Failed: {e}")
        return

    # Export
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.dd2_export.dd2_mesh(filepath=output_path)
        print(f"SUCCESS: Saved to {os.path.basename(output_path)}")
        
        # --- SAFE DELETE SOURCE FILE ---
        try:
            os.remove(filepath)
            print(f">>> DELETED SOURCE: {os.path.basename(filepath)}")
        except Exception as del_e:
            print(f"!!! Could not delete source: {del_e}")
            
    except Exception as e:
        print(f"!!! Export Failed: {e}")

# --- EXECUTION ---
if "--" in sys.argv:
    force_enable_addons()
    args = sys.argv[sys.argv.index("--") + 1:]
    for file_arg in args:
        convert_file(file_arg)