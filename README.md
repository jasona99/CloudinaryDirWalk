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
3. Run the script!
## Potential Issues
* Running the script for more than 1 hour may lead to a stale request error.
  * Cause: Cloudinary has a limit on the amount of time a single set may be used.
  * Workaround: Restart the script.
  * Future considerations:
    * Adding a timer?
