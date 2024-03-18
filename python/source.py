import adsk.core, adsk.fusion, adsk.cam, traceback

def circle():
    return 0

def rectangle():
    # Get the active Fusion 360 application
    app = adsk.core.Application.get()
    if not app:
        raise RuntimeError("Failed to get Fusion 360 application")

    # Get the root component of the active design
    design = app.activeProduct
    root_comp = design.rootComponent
    if not root_comp:
        raise RuntimeError("Failed to get root component")

    # Create a new sketch on the XY plane of the root component
    sketches = root_comp.sketches
    xz_plane = root_comp.xZConstructionPlane
    sketch = sketches.add(xz_plane)
    if not sketch:
        raise RuntimeError("Failed to create sketch")
    

    # Create a rectangle using sketch geometry
    lines = sketch.sketchCurves.sketchLines
    start_point = adsk.core.Point3D.create(0, 0, 0)
    end_point = adsk.core.Point3D.create(10, 0, 0)
    line1 = lines.addByTwoPoints(start_point, end_point)
    end_point = adsk.core.Point3D.create(10, 1, 0)
    line2 = lines.addByTwoPoints(line1.endSketchPoint, end_point)
    end_point = adsk.core.Point3D.create(0, 1, 0)
    line3 = lines.addByTwoPoints(line2.endSketchPoint, end_point)
    line4 = lines.addByTwoPoints(line3.endSketchPoint, line1.startSketchPoint)

    # Create an extrusion feature based on the sketch to form a cube
    extrudes = root_comp.features.extrudeFeatures
    profile = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(10.0)  # Extrusion distance
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    cube = extrudes.add(extrude_input)
    if not cube:
        raise RuntimeError("Failed to create cube")

    # Hide the sketch
    sketch.isVisible = False

def run(context):
    try:
        rectangle()
    except Exception as e:
        print("Failed with exception:")
        print(str(e))
        if hasattr(traceback, 'format_exc'):
            print(traceback.format_exc())

run(adsk.fusion.Design().activeProduct)

def run(context):
    try:
        rectangle()
    except Exception as e:
        print("Failed with exception:")
        print(str(e))
        if hasattr(traceback, 'format_exc'):
            print(traceback.format_exc())

run(adsk.fusion.Design().activeProduct)
