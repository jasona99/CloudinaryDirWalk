import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

def tag_image(file, path):
    tag_list = []

    credentials = service_account.Credentials.from_service_account_file('gcpkey.json')

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # The name of the image file to annotate
    file_name = os.path.join(path, file)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        if len(label.description) >= 1 and label.score >= .5:
            print("Added", label.description, "with a confidence of", label.score)
            tag_list.append(label.description)

    return tag_list
