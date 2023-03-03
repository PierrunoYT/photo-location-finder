import io
import os
import json
from google.cloud import vision
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1.types import Feature
import re


def recognize_landmark(config_path):
    # Parse configuration data from file
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
        api_key = config_data['google_cloud_api_key']
        cred_path = config_data['google_application_credentials_file_path']
        image_dir = config_data.get('image_directory_path', '.')  # new parameter

    # Set environment variables for API key and credentials file path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser(cred_path)
    os.environ["GOOGLE_API_KEY"] = api_key

    # Create a client object
    client = ImageAnnotatorClient()

    # Set up feature types
    feature_landmark = Feature(type_=Feature.Type.LANDMARK_DETECTION)
    feature_label = Feature(type_=Feature.Type.LABEL_DETECTION)
    feature_web = Feature(type_=Feature.Type.WEB_DETECTION)

    # Gathering image files in the directory
    image_files = []
    if os.path.exists(image_dir):
        for filename in os.listdir(image_dir):
            if re.search(r"\.(jpg|jpeg|png)$", filename, re.IGNORECASE):
                image_path = os.path.join(image_dir, filename)
                with open(image_path, 'rb'):
                    pass

                image_files.append(image_path)

    num_images = len(image_files)
    if num_images == 0:
        print("No images found in the specified directory.")
        return

    print(f"{num_images} image files found.")

    # Prompt for confirmation if there are more than 100 images
    if num_images > 100:
        confirm = input(f"WARNING: {num_images} images found. Continue? (y/n): ")
        if not confirm.lower().startswith("y"):
            print("Operation cancelled.")
            return

    result_data = {
        "landmarks": [],
        "labels": [],
        "web_entities": []
    }

    # Process each image file
    for image_path in image_files:
        try:
            # Read the image file
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            # Perform the landmark detection
            response = client.annotate_image({
                'image': image,
                'features': [feature_landmark, feature_label, feature_web],
            })

            if response.error.message:
                raise Exception(f"Error: {response.error.message}")

            # Extract landmark information
            landmarks = response.landmark_annotations
            if landmarks:
                for landmark in landmarks:
                    result_data["landmarks"].append({
                        "file": image_path,
                        "name": landmark.description,
                        "latitude": landmark.locations[0].lat_lng.latitude,
                        "longitude": landmark.locations[0].lat_lng.longitude,
                        "confidence": landmark.score
                    })

            # Extract label information
            labels = response.label_annotations
            if labels:
                for label in labels:
                    result_data["labels"].append({
                        "file": image_path,
                        "label": label.description
                    })

            # Extract web entity information
            web_entities = response.web_detection.web_entities
            if web_entities:
                for entity in web_entities:
                    result_data["web_entities"].append({
                        "file": image_path,
                        "entity": entity.description,
                        "score": entity.score
                    })
        except FileNotFoundError as f:
            print(f"[ERROR]: {f}")
            print(f"Skipping file {image_path}.")
        except Exception as e:
            print(f"[ERROR]: Error processing {image_path}, {e}")

    # Write the result data to a JSON file in pretty print format
    with open("result.json", "w") as result_file:
        json.dump(result_data, result_file, indent=4)

    print(f"Detection completed. Results saved to '{os.path.abspath('result.json')}'.")
    
    
# Example usage
recognize_landmark(config_path=input("Enter the path to your config file: "))
