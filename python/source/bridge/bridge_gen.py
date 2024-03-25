import adsk.core, adsk.fusion, adsk.cam, traceback

def circle():
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
    
    circles = sketch.sketchCurves.sketchCircles
    circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0),2)

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

    # extrudes = root_comp.features.extrudeFeatures
    # profile = sketch.profiles.item(0)
    # distance = adsk.core.ValueInput.createByReal(10.0)  # Extrusion distance
    # extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    # extrude_input.setDistanceExtent(False, distance)
    # cube = extrudes.add(extrude_input)
    # if not cube:
    #     raise RuntimeError("Failed to create cube")

    # Hide the sketch
    # sketch.isVisible = False

#truss
def bridge(end,points, th, ex):
    try :
        #init
        # Get the active Fusion 360 application
        app = adsk.core.Application.get()
        if not app:
            raise RuntimeError("Failed to get Fusion 360 application")
        ui = app.userInterface
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
        
        #int
        lined = []
        lines = sketch.sketchCurves.sketchLines
        curvesToOffset = adsk.core.ObjectCollection.create()

        ##this is for outside lines
        #down
        start_point = adsk.core.Point3D.create(end, 0, 0)
        end_point = adsk.core.Point3D.create(0, 0, 0)
        line = lines.addByTwoPoints(start_point, end_point)
        lined.append(line)
        #other truss lines - outside
        for i in range(len(points[0])):
            end_point = adsk.core.Point3D.create(points[0][i], -points[1][i] , 0)
            line1 = lines.addByTwoPoints(lined[i*3].endSketchPoint, end_point)
            lined.append(line1)
            end_point = adsk.core.Point3D.create(points[0][i], 0, 0)
            line2 = lines.addByTwoPoints(lined[i*3+1].endSketchPoint, end_point)
            lined.append(line2)
            end_point = adsk.core.Point3D.create(points[0][i], -points[1][i] , 0)
            line3 = lines.addByTwoPoints(lined[i*3+2].endSketchPoint, end_point)
            lined.append(line3)
        
        # uping
        end_point = adsk.core.Point3D.create(end, 0, 0)
        line3 = lines.addByTwoPoints(lined[len(points[0])*3].endSketchPoint, end_point)
        lined.append(line3)
        #uped
        # end_point = adsk.core.Point3D.create((w/n)/2, -h, 0)
        # line4 = lines.addByTwoPoints(lined[2*n+1].endSketchPoint, end_point)
        # lined.append(line4)

        curves = sketch.findConnectedCurves(line)
               
        # Create the offset.
        dirPoint = adsk.core.Point3D.create(0, -0.5, 0)
        offsetCurves = sketch.offset(curves, dirPoint, -th)

        for i in range(len(points[0])):
            extrudes = root_comp.features.extrudeFeatures
            profile = sketch.profiles.item(i)
            distance = adsk.core.ValueInput.createByReal(ex)  # Extrusion distance
            extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extrude_input.setDistanceExtent(False, distance)
            cube = extrudes.add(extrude_input)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
      
lists = [[1,2,3,4,5,6,7,8,9],[5,4,3,6,4,3,8,2,4]]

def main():
    bridge(10,lists,0.25,3)

def run(context):
    try:
        main()
    except Exception as e:
        print("Failed with exception:")
        print(str(e))
        if hasattr(traceback, 'format_exc'):
            print(traceback.format_exc())

run(adsk.fusion.Design().activeProduct)