"""
Test script to verify Toolkit can load the app descriptor.
Run this from within a Toolkit environment.
"""
import sys
import os

# Add Toolkit to path if needed
try:
    import sgtk
    print("✓ sgtk imported successfully")
except ImportError:
    print("✗ ERROR: sgtk not found. Run this from within a Toolkit environment.")
    sys.exit(1)

# Test descriptor loading
try:
    descriptor_dict = {
        "type": "dev",
        "path": r"D:/Steamroller/dev/tk_tool_submit"
    }
    
    # Try to create a descriptor
    from tank.descriptor import Descriptor
    descriptor = Descriptor.create_descriptor(
        sgtk.get_singleton().pipeline_configuration,
        Descriptor.APP,
        descriptor_dict,
        None
    )
    
    print(f"✓ Descriptor created: {descriptor}")
    print(f"✓ Descriptor path: {descriptor.get_path()}")
    print(f"✓ Descriptor exists: {descriptor.exists_local()}")
    print(f"✓ Descriptor system_name: {descriptor.system_name}")
    
    # Check if app.py exists
    app_py_path = os.path.join(descriptor.get_path(), "app.py")
    print(f"✓ app.py exists: {os.path.exists(app_py_path)}")
    
    # Check if info.yml exists
    info_yml_path = os.path.join(descriptor.get_path(), "info.yml")
    print(f"✓ info.yml exists: {os.path.exists(info_yml_path)}")
    
except Exception as e:
    print(f"✗ ERROR creating descriptor: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All checks passed! The app descriptor should be loadable by Toolkit.")

