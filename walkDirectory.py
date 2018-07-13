#some basic imports
import os, re, shutil

#cloudinary sdk
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

#import settings file
import settings

#set Cloudinary config
#to add an api key or secret, change this file
settings.set()
#this may need to be run every hour in order to stay logged in

#a tag that may be added to help show origin of images
START_TAG = "mass_uploaded_file"

autotag_flag = False

#Uncomment to enable autotagging.
#autotag_flag = True

#from sample file
#view the last response fron api call
def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

#upload with file path and name, list of tags to be applied
def upload_file(path, file, tag_list):
    print("Uploading", file)
    path = '/'.join(path.split('\\'))
    print(path[2:]+"/"+file)
    if autotag_flag == True:
        response = upload(path[2:]+"/"+file,
                          use_filename = True,
                          folder = path[2:],
                          categorization = "google_tagging",
                          auto_tagging = 0.5,
                          tags = tag_list)
    else:
        response = upload(path[2:]+"/"+file,
                          use_filename = True,
                          folder = path[2:],
                          tags = tag_list)

    #if upload fails, should just create an error and kill the script
    #otherwise, may be necessary to read response here

    #for debugging only:
    dump_response(response)

    #check if response given
    #it seems if anything fails, Cloudinary breaks for us
    if not len(response["public_id"]) > 0:
        return 1
    #reached
    return 0

#develop tags based on directories
#cosider storing rather than resetting
def directory_tags(split_path):
    tag_list = []
    for dirs in split_path:
        tag_list.extend(re.split(r'[//-]+', dirs))
    tag_list.pop(0)
    #Uncomment to add origin tag.
    #tag_list.append(START_TAG)
    return tag_list

#move to ./Backup/Images
#ensures that, if code must be run again, no need to worry about where it left off.
#quicker solution than checking Cloudinary for duplicates
def completed_move(path, file):
    newpath = "./Backup"+path[1:]
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.rename(path+"\\"+file, newpath+"\\"+file)

#get a public id with directories so as to get subdirectories
#with use_filename parameter, should be unnecessary
def get_id(path, file):
    fixed_path = path[1:]
    return fixed_path.replace(" ","-")+"/"+file.replace(" ","-")

#check if Images exists
if (os.path.isdir("Images")):

    #notify of path that will be uploaded
    print("Uploading all images in folders below",os.path.dirname(__file__)+"\Images")

    #tranverse directories
    for root, dirs, files in os.walk("./Images"):
        #break directory into list
        path = root.split(os.sep)
        #print(os.path.basename(root))
        for file in files:
            print(file)
            tags = directory_tags(path)
            #pub_id = get_id(root, file)

            #this line below actually will upload things
            #be wary if testing
            if not file[-2:] == "db":
                upload_code = upload_file(root, file, tags)

                #move completed files
                if upload_code == 0:
                    #move completed files to backup dir
                    completed_move(root, file)
                    print("Complete.")
                else:
                    print("Failed at ",file)

#no images?
else:
    print("Images directory not found.")
