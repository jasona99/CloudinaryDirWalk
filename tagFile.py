import io
import os
from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

def tag_image(file, path, client):
    tag_list = []

    # The name of the image file to annotate
    file_name = os.path.join(path, file)

    # Check if file size exceeds 10MB limit and attempts to optimize
    while (os.stat(file_name).st_size > 10485760):
        print("**File too large, will attempt to optimize.**")
        
        # Load image
        pil_image = Image.open(file_name)

        # Cut height/width in half, applying magic of antialiasing!
        new_width = int(pil_image.size[0]/2)
        new_height = int(pil_image.size[1]/2)
        pil_image = pil_image.resize((new_width,new_height), Image.ANTIALIAS)

        # Save and optimize, quality at 95%
        pil_image.save("tmp.jpg", optimize=True, quality=95)
        file_name = "tmp.jpg"

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