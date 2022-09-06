from exiftool import ExifToolHelper
with ExifToolHelper() as et:
    filename = "input/DJI_0177.JPG"
    for d in et.get_metadata(filename):
        for k, v in d.items():
            print(f"Dict: {k} = {v}")

