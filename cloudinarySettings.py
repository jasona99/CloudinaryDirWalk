from cloudinary import config
import json

def set():
    with open('cloudinarykey.json', 'r') as f:
        config_json = json.load(f)
    config(
        cloud_name = config_json["cloud_name"],
        api_key = config_json["api_key"],
        api_secret = config_json["api_secret"]
    )
