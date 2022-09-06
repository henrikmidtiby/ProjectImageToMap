import cv2
from exiftool import ExifToolHelper


class CameraPoseFromExif():
    def __init__(self):
        pass
        self.yaw = None
        self.pitch = None
        self.roll = None
        self.latitude = None
        self.longitude = None
        self.altitude = None

    def extract_data_from_image(self, filename):
        with ExifToolHelper() as et:
            try:
                tags = et.get_metadata(filename)[0]
                self.yaw = tags["XMP:GimbalYawDegree"]
                self.roll = tags["XMP:GimbalRollDegree"]
                self.pitch = tags["XMP:GimbalPitchDegree"]
                self.altitude = tags["XMP:RelativeAltitude"]
                self.latitude = tags["Composite:GPSLatitude"]
                self.longitude = tags["Composite:GPSLongitude"]
                #"XMP:AbsoluteAltitude"
                #"EXIF:ExifImageWidth"
                #"EXIF:ExifImageHeight"
                #"XMP:CalibratedFocalLength"
                #"XMP:CalibratedOpticalCenterX"
                #"XMP:CalibratedOpticalCenterY"
            except Exception as e: 
                print("Failed extracting exif information from image")
                print(e)

    def __repr__(self):
        return f"{self.latitude} {self.longitude} {self.altitude} {self.yaw} {self.pitch:8.3f} {self.roll}"


def main(filename):
    cpfe = CameraPoseFromExif()
    cpfe.extract_data_from_image(filename)
    print(cpfe)



filename = "input/DJI_0177.JPG"
main(filename)
