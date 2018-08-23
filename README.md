# CloudinaryDirWalk
Recursively "walks" through an ./Images directory containing only images, looking for images to upload to Cloudinary.
Utilizes JSON files for settings.
If utilizing the code yourself, be sure to add the files for authentication for both Cloudinary and GCP.
## Requirements
* A number of images in sorted folders already
* Python 3.x (built and tested on 3.5)
* Cloudinary SDK
  * PIP install recommended. Package named cloudinary.
* Cloudinary API key/secret in a JSON.
* Google Cloud Platform account with Vision API enabled
  * PIP install recommended. Package named google-cloud.
* Pillow for image shrinking if over 10MB
  * PIP install recommended. Package named pillow.
## Using the script
1. Place the script in a directory also containing an Images directory.
    1. All images should be in directories under this folder.
2. Add the JSON file for the Google Cloud Service Account renamed to gcpkey.json, make one for Cloudinary containing keys for cloud_name, api_key, and api_secret named cloudinarykey.json.
3. Run the script titled walkDirectory.py!
## How it works
1. The main script captures the necessary keys, secrets, and addresses from supporting files.
2. A quick test is run to determine OS. Unfortunately, this is required to ensure the upload path is correct. This is mainly because Windows is annoying.
3. If the image directory exists, a loop begins that will go through each directory and file individually within the Images folder.
4. Within the loop, path formatting occurs, the file is checked to be an image (blacklist used in this case due to known unwanted files, might be appropriate to change to a whitelist).
5. The image, based on the directory, gains tags. Each directory is treated as a tag and any directory with a dash (-) is split at that character.
6. If the directory is set for autotagging in the flag on line 32, the image path will be sent to the tagFile script and run. 5 attempts will be made to retrieve tags. Any fail will be logged.
  1. Autotagging utilizes Google Cloud Vision and the Cloud SDK to upload an image after it is passed to the script.
  2. After the creation of a client, the image's size is checked. If over 10 MB (the Google Cloud Vision upload limit through the SDK), Python Image Library from the pillow package will be used to half the height and width of an image, add antialiasing, then save at 95% quality as a temp file outside of the Images directory. This will then be used for autotagging only.
  3. The image is opened and passed to Google Cloud Vision.
  4. The response is collected and passed back to the main script as a list if the confidence score is over .5.
7. 3 attempts are made to upload to Cloudinary. Any failures are logged. Cloudinary will also leave the response code in the log file for each file, showing the error.
8. If the upload is successful to Cloudinary, the image is moved to a Backup folder outside of the Images directory (in the directory of the script, if possible). A backup folder is created, if necessary.
## Potential Issues
* ~~Running the script for more than 1 hour may lead to a stale request error.~~
  * ~~Cause: Cloudinary has a limit on the amount of time a single set may be used.~~
  * ~~Workaround: Restart the script.~~
  * ~~Future considerations:~~
    * ~~Adding a timer?~~
  * Determined to be a non-issue on full run.
