

from os import mkdir, scandir, rename as move_file, path
from os.path import isdir
from PIL import Image, UnidentifiedImageError
from pillow_heif import open_heif
from datetime import datetime
import utils

photos_dir = "D:\\Photos"
delimiter = "\\"
specific_folder_name = "TEST_DELETE_AFTER"
photo_dump_folder = photos_dir + delimiter + specific_folder_name

"""turns .*yyyy:mm:dd.* into yyyy-mm-dd"""
def extractDateFromRawExif(raw_string):
    first_colon_index = raw_string.index(":") 
    date = raw_string[first_colon_index - 4 : first_colon_index + 6]
    return date.replace(":", "-").strip()

def getDefaultExifDate(path_to_photo):
    image_file = Image.open(path_to_photo)
    exif = image_file.getexif()
    raw_exif_date = exif[306]
    return extractDateFromRawExif(raw_exif_date)

def getHeifExifDate(path_to_photo):
    heif_info = open_heif(path_to_photo).info
    exif = str(heif_info['exif'])
    return extractDateFromRawExif(exif)

"""gets photo EXIF data date taken from any file, returns as hyphenated string"""
def getExifDate(path_to_photo):
    file_type = path_to_photo.split(".")[-1].lower()
    if (file_type == "heic"):
        try:
            return getHeifExifDate(path_to_photo)
        except ValueError: #tricky little file isn't actually a HEIF... convert normally
           return getDefaultExifDate(path_to_photo)
        
    else: # all other file types
        return getDefaultExifDate(path_to_photo)

def getModifiedDate(path_to_photo):
    epoch = path.getmtime(path_to_photo)
    raw_modified_time = str(datetime.fromtimestamp(epoch))
    return raw_modified_time.split()[0].strip()

if __name__ == "__main__":

    log_file_name = utils.gen_log_file_name()
    log_file = open("logs/" + log_file_name, "w")

    if not isdir(photo_dump_folder):
        print("\nbad directory; " + photo_dump_folder + " does not exist\n")
        exit()

    fso_iterator = scandir(photo_dump_folder)

    for fso in fso_iterator:

        if (fso.is_file()):
            
            file_name = fso.name
            src_photo_path = photo_dump_folder + delimiter + file_name

            try:
                photo_date = getExifDate(src_photo_path)
            except KeyError: # PNGs & screenshots don't have exif data
                photo_date = getModifiedDate(src_photo_path)
            except UnidentifiedImageError: #could be a video or something else
                photo_date = getModifiedDate(src_photo_path)


            # uncomment one of the following lines to send the photos to either a subfolder of the original dump folder, or to a generic dest (ideally it would be subfoldered by /year/month)
            dest_folder_path = photo_dump_folder + delimiter + str(photo_date)
            # dest_folder_path = photos_dir + delimiter + str(photo_date)
            
            folder_exists = isdir(dest_folder_path)
            if not folder_exists:
                mkdir(dest_folder_path)

            dest_photo_path = dest_folder_path + delimiter + file_name

            log_file.write(file_name + ": " + src_photo_path + " -> " + dest_photo_path)

            # TODO identify duplicates, do not attempt move if a duplicate is found
            
            try:
                move_file(src_photo_path, dest_photo_path)
            except FileExistsError:
                print(dest_folder_path)

    log_file.close()