from exiftool import ExifToolHelper
with ExifToolHelper() as et:
    filename = "input/DJI_0177.JPG"
    for d in et.get_metadata(filename):
        for k, v in d.items():
            print(f"Dict: {k} = {v}")


    print("Testing")
    tags = et.get_metadata(filename)

    keys = ["XMP:GimbalRollDegree",
            "XMP:GimbalPitchDegree", 
            "XMP:GimbalYawDegree",
            "XMP:CalibratedFocalLength", 
            "XMP:CalibratedOpticalCenterX", 
            "XMP:CalibratedOpticalCenterY",
            "Composite:GPSLatitude",
            "Composite:GPSLongitude",
            "XMP:AbsoluteAltitude",
            "XMP:RelativeAltitude"]


    for key in keys:
        try:
            print(f"{ key } = { tags[0][key] }")
        except:
            pass
