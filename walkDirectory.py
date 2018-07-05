import os, re
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

#import settings file
import settings

#set Cloudinary config
#to add an api key or secret, change this file
settings.set()
#this may need to be run every hour in order to stay logged in

START_TAG = "mass_uploaded_file"

#from sample file
#view the last response fron api call
def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

#upload with file path and name, list of tags to be applied
def upload(file, tag_list, public_id):
    print("Uploading", file)
    response = upload(file, tags = tag_list)
    #if upload fails, should just create an error and kill the script
    #otherwise, may be necessary to read response here

    #for debugging only:
    dump_response(response)

    #reached end, safety print
    print("Complete!")

def directory_tags(split_path):
    tag_list = []
    for dirs in split_path:
        tag_list.extend(re.split(r'[//-]+', dirs))
    tag_list.pop(0)
    return tag_list

def completed_move(path, file):
    newpath = "./Backup"+path[1:]
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.rename(path+"\\"+file, newpath+"\\"+file)
    print("Moved.")


def get_id(path, file):
    fixed_path = path[1:]
    return fixed_path + "\\" + file

#check if Images exists
if (os.path.isdir("Images")):

    #notify of path that will be uploaded
    print("Uploading all images in folders below",os.path.dirname(__file__)+"\Images")

    #tranverse directories
    for root, dirs, files in os.walk(".\\Images\\"):
        #break directory into list
        path = root.split(os.sep)
        print(os.path.basename(root))
        for file in files:
            print(file)
            tags = directory_tags(path)
            print(tags)
            pub_id = get_id(root, file)
            print(pub_id)

            #this line below actually will upload things
            #be wary if testing
            #upload(file, tags, pub_id)

            #move completed files
            completed_move(root, file)


else:
    print("Images directory not found.")
