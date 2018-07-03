import os
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import resources_by_tag

#import settings file
import settings
#set api key in Cloudinary config
settings.set()
