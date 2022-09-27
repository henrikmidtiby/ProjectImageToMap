from exiftool import ExifToolHelper
with ExifToolHelper() as et:
    filename = "input/DJI_0177.JPG"
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
            "XMP:RelativeAltitude",
            "EXIF:ExifImageWidth",
            "EXIF:ExifImageHeight"]


    for key in keys:
        try:
            print(f"{ key } = { tags[0][key] }")
        except:
            pass
