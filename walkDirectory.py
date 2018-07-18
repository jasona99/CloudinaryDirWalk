#some basic imports
import os, sys, re, shutil, time, logging

#cloudinary sdk
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from google.oauth2 import service_account
from google.cloud.vision import types
from google.cloud import vision

credentials = service_account.Credentials.from_service_account_file('gcpkey.json')
gcp_client = vision.ImageAnnotatorClient(credentials=credentials)

#importing method to tag
import tagFile

#import settings file
import cloudinarySettings

#set Cloudinary config
#to add an api key or secret, change this file
cloudinarySettings.set()
#this may need to be run every hour in order to stay logged in

#prepare to logging
logging.basicConfig(filename="dirwalk.log", level=logging.DEBUG)

#a tag that may be added to help show origin of images
START_TAG = "mass_uploaded_file"

autotag_flag = True



#Check if running Windows.
win_os = False

def get_os():
    global win_os
    if os.name == "nt":
        print("Note: Running Windows!")
        win_os = True
        time.sleep(3)
    else:
        print("Note: Not running Windows!")
        win_os = False
        time.sleep(3)

#Uncomment to enable autotagging.
#autotag_flag = True

#from sample file
#view the last response fron api call
def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

#upload with file path and name, list of tags to be applied
def upload_file(path, filename, tag_list):
    print("Uploading", file)
    if win_os == True:
        path = '/'.join(path.split('\\'))
    print(path[2:]+"/"+filename)

    #check autotag flag
    #if autotag_flag == True:

    #use sdk upload function with params
    response = upload(path[2:]+"/"+file,
                      use_filename = True,
                      folder = path[2:],
                      tags = tag_list)
    """else:
        #use sdk upload function with params
        response = upload(path[2:]+"/"+file,
                          use_filename = True,
                          folder = path[2:],
                          tags = tag_list)
    """

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

#get gcp autotags from defined gcp account
#WARNING: Will cost!!!
def get_autotag(file, path):
    print(path, file)
    tags = tagFile.tag_image(file, path, gcp_client)
    return tags

#move to ./Backup/Images
#ensures that, if code must be run again, no need to worry about where it left off.
#quicker solution than checking Cloudinary for duplicates
def completed_move(path, filename):
    newpath = "./Backup"+path[1:]
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    if win_os:
        os.rename(path+"\\"+filename, newpath+"\\"+filename)
    else:
        os.rename(path+"/"+filename, newpath+"/"+filename)

#get a public id with directories so as to get subdirectories
#with use_filename parameter, should be unnecessary
def get_id(path, file):
    fixed_path = path[1:]
    return fixed_path.replace(" ","-")+"/"+file.replace(" ","-")

#check if Images exists
if (os.path.isdir("Images")):

    #notify of path that will be uploaded
    print("Uploading all images in folders below",os.path.dirname(__file__)+"\Images")

    #check os
    get_os()

    #tranverse directories
    for root, dirs, files in os.walk("./Images"):
        #break directory into list
        path = root.split(os.sep)
        #print(os.path.basename(root))
        for file in files:
            print(file)

            #Get tags based on directory
            tags = directory_tags(path)

            #pub_id = get_id(root, file)

            #this line below actually will upload things
            #be wary if testing
            if not file[-2:] == "db" and not file.startswith(".") and not file[-3:] == "zip" and not file[-3:] == "MOV" and not file[-3:] == "mov":

                #Add autotags if flag is set to true.
                if autotag_flag:
                    #Retry 10 times.
                    for attempt in range(5):
                        #Attempt to connect to GCP and get tags.
                        try:
                            print("Trying!")
                            tags.extend(get_autotag(file, root))
                            break
                        #Error
                        except:
                            #Log and move on if limit reached.
                            if attempt == 4:
                                print("All attempts failed, logging and moving on without adding autotags to file.")
                                logging.warning("GCP was unable to handle "+file+" in "+root+" at attempt "+str(attempt)+".")
                                continue
                            else:
                                print("ERROR IN GOOGLE CLOUD PLATFORM. Waiting 5 seconds then retrying. Attempt ",str(attempt))
                                time.sleep(5)



                for attempt in range(3):
                    #Attempt to connect to cloudinary and upload
                    try:
                        upload_code = upload_file(root, file, tags)
                        break
                    #Error
                    except:
                        #Log and move on if attempt limit reached.
                        if attempt == 2:
                            print("All attempts failed to upload file, logging and moving on without uploading.")
                            logging.warning("Cloudinary was unable to handle "+file+" in "+root+".")
                            continue
                        else:
                            print("ERROR IN Cloudinary. Waiting 5 seconds then retrying. Attempt ",str(attempt))
                            time.sleep(5)


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
