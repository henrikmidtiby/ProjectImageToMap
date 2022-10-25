import cv2
import numpy as np
from exiftool import ExifToolHelper
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import Affine
import utm
import argparse
from icecream import ic


class CameraInformationFromExif():
    def __init__(self):
        pass
        self.yaw = None
        self.pitch = None
        self.roll = None
        self.latitude = None
        self.longitude = None
        self.altitude = None

        self.cx = None
        self.cy = None
        self.focallength = 2500
        self.image_width = None
        self.image_height = None

    def extract_data_from_image(self, filename):
        with ExifToolHelper() as et:
            try:
                tags = et.get_metadata(filename)[0]
                self.yaw = float(tags["XMP:GimbalYawDegree"])
                self.roll = float(tags["XMP:GimbalRollDegree"])
                self.pitch = float(tags["XMP:GimbalPitchDegree"])
                self.altitude = float(tags["XMP:RelativeAltitude"])
                self.latitude = float(tags["Composite:GPSLatitude"])
                self.longitude = float(tags["Composite:GPSLongitude"])
                self.image_width = float(tags["EXIF:ExifImageWidth"])
                self.image_height = float(tags["EXIF:ExifImageHeight"])
                self.focallength = float(tags["XMP:CalibratedFocalLength"])
                self.cx = float(tags["XMP:CalibratedOpticalCenterX"])
                self.cy = float(tags["XMP:CalibratedOpticalCenterY"])
            except Exception as e: 
                print()
                print("=============================================")
                print("Failed extracting exif information from image")
                print("=============================================")
                print()
                print(e)

    def get_values_from_arguments(self, args):
        if args.yaw is not None:
          self.yaw = args.yaw
        if args.pitch is not None:
          self.pitch = args.pitch
        if args.roll is not None:
          self.roll = args.roll
        if args.latitude is not None:
          self.latitude = args.latitude
        if args.longitude is not None:
          self.longitude = args.longitude
        if args.altitude is not None:
          self.altitude = args.altitude
        if args.cx is not None:
          self.cx = args.cx
        if args.cy is not None:
          self.cy = args.cy
        if args.focallength is not None:
          self.focallength = args.focallength
        if args.image_width is not None:
          self.image_width = args.image_width
        if args.image_height is not None:
          self.image_height = args.image_height

    def __repr__(self):
        return f"{self.latitude} {self.longitude} {self.altitude} {self.yaw} {self.pitch:8.3f} {self.roll}"


class ProjectImageToGround():
    def __init__(self): 
        pass

    def set_camera_information(self, camera_information):
        self.camera_information = camera_information

    def calculate_projection_transform(self):

        # Calculations all take place in the Universal Transverse Mercator (UTM)
        # coordinate system \addref{}, where $x$ is displacement towards east,
        # $y$ is displacement towards north and $z$ is the altitude above sea level.
    
        # The orientation of the camera is described by
        # the three rotation angles: $yaw$, $pitch$ and $roll$.
        # Assuming that the camera is pointing towards the horizon,
        # the \emph{yaw} values is the compass heading that the camera is looking towards,
        # e.g. $yaw = 0\degree$ is towards north and $yaw = 45\degree$ is towards north east.
        # The camera $pitch$ is the angle of the camera relative to the horizon,
        # when $pitch = 0\degree$ the camera is looking directly forward and when
        # $pitch = -90\degree$ the camera is looking directly towards the ground.
        # The $roll$ values is how much the horizon is away from being horizontal;
        # this will in practice often be zero as the camera gimbal ensures that.
    
    
        def get_yaw_matrix(yaw_angle):
            return np.array([[np.cos(yaw_angle), np.sin(yaw_angle), 0],
                             [-np.sin(yaw_angle), np.cos(yaw_angle), 0],
                             [0, 0, 1]])
    
    
        def get_pitch_matrix(pitch_angle):
            return np.array([[1, 0, 0],
                             [0, np.cos(pitch_angle), -np.sin(pitch_angle)],
                             [0, np.sin(pitch_angle), np.cos(pitch_angle)]])
    
    
        def get_roll_matrix(roll_angle):
            return np.array([[np.cos(roll_angle), 0, np.sin(roll_angle)],
                             [0, 1, 0],
                             [-np.sin(roll_angle), 0, np.cos(roll_angle)]])
    
    
        # Yaw is rotation around the $z$ axis (up / down)
        yaw_matrix = get_yaw_matrix(yaw_angle=-self.camera_information.yaw * np.pi / 180)
    
        # Pitch is rotation around the x axis (right / left)
        pitch_matrix = get_pitch_matrix(pitch_angle=self.camera_information.pitch * np.pi / 180)
    
        # Roll is rotation around the y axis (forward / back)
        roll_matrix = get_roll_matrix(roll_angle=self.camera_information.roll * np.pi / 180)
    
        R_pose = np.matmul(yaw_matrix, np.matmul(pitch_matrix, roll_matrix))
    
        iw = self.camera_information.image_width
        ih = self.camera_information.image_height
        dfl = 2*self.camera_information.focallength
        im_points = np.array([[-iw / dfl, 1, -ih / dfl],
                              [-iw / dfl, 1, ih / dfl],
                              [iw / dfl, 1, ih / dfl],
                              [iw / dfl, 1, -ih / dfl],
                              [-iw / dfl, 1, -ih / dfl]])
        im_points = np.transpose(im_points)
        directions = np.matmul(R_pose, im_points)
    
        # Project image plane on the ground
        altitude = self.camera_information.altitude
        down = np.array([[0, 0, -1]])
    
        z_components = np.matmul(down, directions)
        scaling_factors = altitude / z_components
        scaling_factor_matrix = np.diag(scaling_factors[0])
        corners_on_ground = np.matmul(directions, scaling_factor_matrix)
    
        # Determine perspective transform from image plane to ground plane
    
        image_corners = np.float32([
                [self.camera_information.image_width, self.camera_information.image_height], 
                [self.camera_information.image_width, 0],
                [0, 0], 
                [0, self.camera_information.image_height], 
                ])
        transformed_image_corners_raw = corners_on_ground[0:2, 0:4].transpose().astype(np.float32) / self.GSD
        lower_bb_coord = transformed_image_corners_raw.min(0)
        higher_bb_coord = transformed_image_corners_raw.max(0)
        bb_size = np.ceil(higher_bb_coord - lower_bb_coord)
        transformed_image_corners = transformed_image_corners_raw - np.repeat([lower_bb_coord], 4, axis=0)
    
        resmatrix = cv2.getPerspectiveTransform(image_corners, transformed_image_corners)
        return resmatrix, bb_size, lower_bb_coord, transformed_image_corners_raw
    



def handle_image(cife, input_filename, output_filename, gsd):
    pitg = ProjectImageToGround()
    pitg.set_camera_information(cife)
    pitg.GSD = gsd
    resmatrix, bb_size, lower_bb_coord, transformed_image_corners_raw = pitg.calculate_projection_transform()
    lower_bb_coord = transformed_image_corners_raw.min(0)
    higher_bb_coord = transformed_image_corners_raw.max(0)


    img = cv2.imread(input_filename)
    result_image_size = (int(bb_size[0]), int(bb_size[1]))
    resultimage = cv2.warpPerspective(img, resmatrix, result_image_size)
    cv2.imwrite("output/05transformed_image.jpg", resultimage)
    result_image_rotated = cv2.rotate(resultimage, cv2.ROTATE_180)
    cv2.imwrite("output/05transformed_image_rotated.jpg", result_image_rotated)


    Z = result_image_rotated.transpose(2, 0, 1)
    res = pitg.GSD # Resolution
    # global position of upper left corner (x, y)
    print(utm.from_latlon(cife.latitude, cife.longitude))
    x, y, Number, zone = utm.from_latlon(cife.latitude, cife.longitude)
    x = x + 0.5 * res - higher_bb_coord[0] * res # East - West
    y = y - 0.5 * res + higher_bb_coord[1] * res # North - South
    # x is east / west direction
    x = x + 0.5 * res - bb_size[1] / 2 
    # y is north / south direction
    y = y - 0.5 * res + bb_size[0] / 2
    transform = Affine.translation(x, y) * Affine.scale(res, -res)
    with rasterio.open(
        output_filename,
        'w',
        driver='GTiff',
        height=Z.shape[1],
        width=Z.shape[2],
        count=3,
        dtype=Z.dtype,
        crs=rasterio.crs.CRS.from_epsg(32632), # UTM 32N - This matches well here in Denmark.
        transform=transform,
        nodata=0,
        compress='lzw',
    ) as dst:
        dst.write(Z)

    
def main():
    parser = argparse.ArgumentParser(description='Project image down to ground plane')
    parser.add_argument('input_filename', type=str,
                        help='path to file')
    parser.add_argument('output_filename', type=str,
                        help='path to file (include .tif)')
    parser.add_argument('--pose_image', type=str,
                        help='Specify path to image which camera pose should be used for the projection.')
    parser.add_argument('--gsd', type=float, default=0.05, 
                        help='ground sample distance in meters')
    parser.add_argument('--yaw', type=float,
                        help='')
    parser.add_argument('--pitch', type=float,
                        help='')
    parser.add_argument('--roll', type=float,
                        help='')
    parser.add_argument('--latitude', type=float,
                        help='')
    parser.add_argument('--longitude', type=float,
                        help='')
    parser.add_argument('--altitude', type=float,
                        help='')
    parser.add_argument('--cx', type=float,
                        help='')
    parser.add_argument('--cy', type=float,
                        help='')
    parser.add_argument('--focallength', type=float,
                        help='')
    parser.add_argument('--image_width', type=float,
                        help='')
    parser.add_argument('--image_height', type=float,
                        help='')
    

    args = parser.parse_args()

    cife = CameraInformationFromExif()
    if(args.pose_image is None):
      cife.extract_data_from_image(args.input_filename)
    else:
      cife.extract_data_from_image(args.pose_image)
    cife.get_values_from_arguments(args)

    handle_image(cife, args.input_filename, args.output_filename, args.gsd)


main()
    

