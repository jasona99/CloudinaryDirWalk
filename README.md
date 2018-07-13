# CloudinaryDirWalk
Recursively "walks" through an ./Images directory containing only images, looking for images to upload to Cloudinary.
Utilizes a settings.py file with a set() method to define configuration options.
If utilizing the code yourself, be sure to add API key and secret to that.
## Requirements
* A number of images in sorted folders already
* Python 3.x (built and tested on 3.5)
* Cloudinary SDK
  * PIP install recommended. Package named cloudinary.
* Cloudinary API key/secret.
## Using the script
1. Place the script in a directory also containing an Images directory.
    1. All images should be in directories under this folder.
2. Update settings.py with necessary API material.
3. Run the script!
## Sample settings.py file
    from cloudinary import config

    def set():
        config(
            cloud_name = "test-name",
            api_key="12345678",
            api_secret = "SecretKeyProvided"
        )
Though Cloudinary does suggest putting the data in path, seemed less than ideal for the use case.
## Potential Issues
* Running the script for more than 1 hour may lead to a stale request error.
  * Cause: Cloudinary has a limit on the amount of time a single set may be used.
  * Workaround: Restart the script.
  * Future considerations:
    * Adding a timer?
