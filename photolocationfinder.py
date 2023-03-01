import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1.types import Feature

def recognize_landmark():
    """Detects landmarks in the given image."""
    # Prompt the user for the image path, API key, and credentials
    while True:
        try:
            image_path = input("Enter the path to the image file: ")
            with open(image_path, 'rb'):
                pass
            break
        except FileNotFoundError:
            print(f"File not found at '{image_path}'. Please enter a valid file path.")
            
    while True:
        api_key = input("Enter your Google Cloud API key: ")
        if api_key:
            break
        print("API key is required. Please enter a valid API key.")

    while True:
        cred_path = input("Enter the path to your Google Cloud credentials file: ")
        if os.path.isfile(cred_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser(cred_path)
            break
        print(f"File not found at '{cred_path}'. Please enter a valid file path.")

    # Create a client object
    client = ImageAnnotatorClient()

    # Read the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Set the type of features to be performed
    # Options are: LANDMARK_DETECTION, LOGO_DETECTION, LABEL_DETECTION, WEB_DETECTION
    # See https://googleapis.dev/python/vision/latest/gapic/v1/types.html#google.cloud.vision_v1.types.Feature.Type
    feature_landmark = Feature(type_=Feature.Type.LANDMARK_DETECTION)
    feature_label = Feature(type_=Feature.Type.LABEL_DETECTION)
    feature_web = Feature(type_=Feature.Type.WEB_DETECTION)

    # Perform the landmark detection
    response = client.annotate_image({
        'image': image,
        'features': [feature_landmark, feature_label, feature_web],
    })

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: '
                        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))

    # Print the landmark information
    landmarks = response.landmark_annotations
    if landmarks:
        for landmark in landmarks:
            print('Landmark name:', landmark.description)
            print('Latitude:', landmark.locations[0].lat_lng.latitude)
            print('Longitude:', landmark.locations[0].lat_lng.longitude)
            print('Confidence:', landmark.score)
    else:
        print('No landmarks detected.')
        
    # Print the label information
    labels = response.label_annotations
    if labels:
        print('\nLabels:')
        for label in labels:
            print(label.description)
    else:
        print('No labels detected.')
        
    # Print the web information
    web_entities = response.web_detection.web_entities
    if web_entities:
        print('\nWeb entities:')
        for entity in web_entities:
            print(entity.description)
    else:
        print('No web entities detected.')


# Example usage
recognize_landmark()
