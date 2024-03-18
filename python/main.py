import adsk.core, adsk.fusion, adsk.cam, traceback
import source

def run(context):
    try:
        source.rectangle()
    except Exception as e:
        print("Failed with exception:")
        print(str(e))
        if hasattr(traceback, 'format_exc'):
            print(traceback.format_exc())

run(adsk.fusion.Design().activeProduct)
