import os
import json
import asyncio
from pathlib import Path

import aiohttp
from google.cloud import vision_v1
from google.cloud.vision_v1.types import Feature


def read_config(config_path):
    """Reads configuration data from file."""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    try:
        with config_file.open('r') as f:
            config_data = json.load(f)
            api_key = config_data['google_cloud_api_key']
            cred_path = config_data.get('google_application_credentials_file_path')
            image_dir = config_data.get('image_directory_path', '.')
            prompt_for_confirmation = config_data.get('prompt_for_confirmation', False)

        return api_key, cred_path, image_dir, prompt_for_confirmation
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid configuration file format: {e}")


async def process_image(image_path, client, api_key):
    """Processes a single image using the given client."""
    try:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision_v1.Image(content=content)
        features = [
            Feature(type=Feature.Type.LANDMARK_DETECTION),
            Feature(type=Feature.Type.LABEL_DETECTION),
            Feature(type=Feature.Type.WEB_DETECTION)
        ]
        response = await client.annotate_image({
            'image': image,
            'features': features,
        })

        if response.error.message:
            raise Exception(f"[VISION API ERROR] - {response.error.message}")

        result_data = {"filename": image_path, "landmarks": [], "labels": [], "web_entities": []}

        landmarks = response.landmark_annotations
        if landmarks:
            for landmark in landmarks:
                result_data["landmarks"].append({"name": landmark.description,
                                                 "latitude": landmark.locations[0].lat_lng.latitude,
                                                 "longitude": landmark.locations[0].lat_lng.longitude,
                                                 "confidence": landmark.score})
        else:
            # If no landmarks were detected, try reverse geocoding based on object labels
            object_labels = [label.description.lower() for label in response.label_annotations[:3]]
            location = await get_location_from_google_maps_api(object_labels, api_key)
            if location:
                result_data["location"] = location

        labels = response.label_annotations
        if labels:
            for label in labels:
                result_data["labels"].append({"label": label.description})

        web_entities = response.web_detection.web_entities
        if web_entities:
            for entity in web_entities:
                result_data["web_entities"].append({"entity": entity.description, "score": entity.score})

        print(f"[INFO]: Successfully processed image '{image_path}'")
        return result_data

    except FileNotFoundError as f:
        print(f"[IO ERROR][Image '{image_path}']: {f}")
    except Exception as e:
        print(f"[PROCESSING ERROR][Image '{image_path}']: {e}")
        return {}

async def get_location_from_google_maps_api(object_labels, api_key):
    """Uses Google Maps API to get the approximate location of the landmark based on its appearance."""
    query = " ".join(object_labels)
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=geometry&key={api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                data = await response.json()
                if data["candidates"]:
                    location = data["candidates"][0]["geometry"]["location"]
                    return location
    return {}


def get_files_by_extension(directory, extensions):
    """Returns a list of files in directory that match one or more extensions."""
    files = []
    for ext in extensions:
        files.extend(Path(directory).glob(f"*.{ext}"))
    return files


def main():
    """
    A function that processes images in a given directory and extracts landmark,
    label and web entity information using Google Cloud Vision API. The result is
    dumped into a JSON file in pretty print format.
    """
    config_path = 'config.json'
    api_key, cred_path, image_dir, prompt_for_confirmation = read_config(config_path)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
    client = vision_v1.ImageAnnotatorClient()

    image_files = get_files_by_extension(image_dir, ["png", "jpg", "jpeg"])
    num_images = len(image_files)
    if num_images == 0:
        print("No images found in the specified directory.")
        return

    print(f"{num_images} image files found.")

    # Prompt for confirmation if there are more than 100 images
    if num_images > 100 and prompt_for_confirmation:
        confirm = input(f"WARNING: {num_images} images found. Continue? (y/n): ")
        if not confirm.lower().startswith("y"):
            print("Operation cancelled.")
            return

    result_data = []
    # Process each image using asyncio tasks
    tasks = [asyncio.create_task(process_image(str(img_f), client, api_key)) for img_f in image_files]
    results = asyncio.run(asyncio.gather(*tasks))
    result_data = [data for data in results if data != {}]

    # Write the result data to a JSON file in pretty print format
    result_file = Path('result.json')
    with result_file.open("w") as f:
        json.dump(result_data, f, indent=4)

    print(f"Detection completed. Results saved to '{result_file.absolute()}'.")


if __name__ == '__main__':
    main()
