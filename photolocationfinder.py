import asyncio
import os
import json
from pathlib import Path

import aiohttp
from google.cloud import vision_v1
from google.cloud.vision_v1.types import Feature

class ImageProcessor:
    def __init__(self, api_key, cred_path, image_dir, prompt_for_confirmation):
        self.api_key = api_key
        self.cred_path = cred_path
        self.image_dir = image_dir
        self.prompt_for_confirmation = prompt_for_confirmation
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.cred_path
        self.client = None

    async def initialize_client(self):
        if self.client is None:
            self.client = vision_v1.ImageAnnotatorClient()

    async def process_image(self, image_path: str):
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
            response = self.client.annotate_image({
                'image': image,
                'features': features,
            })

            if response.error.message:
                raise Exception(f"[VISION API ERROR] - {response.error.message}")

            result_data = {"filename": image_path, "landmarks": [], "labels": [], "web_entities": []}

            landmarks = response.landmark_annotations
            if landmarks:
                for landmark in landmarks:
                    result_data["landmarks"].append({
                        "name": landmark.description,
                        "latitude": landmark.locations[0].lat_lng.latitude,
                        "longitude": landmark.locations[0].lat_lng.longitude,
                        "confidence": landmark.score
                    })
            else:
                # If no landmarks were detected, try reverse geocoding based on object labels
                object_labels = [label.description.lower() for label in response.label_annotations[:3]]
                location = await self.get_location_from_google_maps_api(object_labels)
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
            raise Exception(f"[IO ERROR][Image '{image_path}']: {f}") from f
        except Exception as e:
            raise Exception(f"[PROCESSING ERROR][Image '{image_path}']: {e}")

    async def get_location_from_google_maps_api(self, object_labels: list[str]):
        """Uses Google Maps API to get the approximate location of the landmark based on its appearance."""
        query = " ".join(object_labels)
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=geometry&key={self.api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.ok:
                    data = await response.json()
                    if data.get("candidates"):
                        location = data["candidates"][0]["geometry"]["location"]
                        return location
        return None

    def get_files_by_extension(self, extensions: list[str]):
        """Returns a list of files in directory that match one or more extensions."""
        files = []
        for ext in extensions:
            files.extend(Path(self.image_dir).glob(f"*.{ext}"))
        return files

    async def detect_objects_in_images(self):
        await self.initialize_client()
        image_files = self.get_files_by_extension(["png", "jpg", "jpeg"])
        num_images = len(image_files)
        if num_images == 0:
            print("No images found in the specified directory.")
            return

        print(f"{num_images} image files found.")

        # Prompt for confirmation if there are more than 100 images
        if num_images > 100 and self.prompt_for_confirmation:
            confirm = input(f"WARNING: {num_images} images found. Continue? (y/n): ")
            if not confirm.lower().startswith("y"):
                print("Operation cancelled.")
                return

        result_data = []
        # Process each image using asyncio tasks
        tasks = [asyncio.create_task(self.process_image(str(img_f))) for img_f in image_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        result_data = [data for data in results if isinstance(data, dict)]

        # Write the result data to a JSON file in pretty print format
        result_file = Path('result.json')
        with result_file.open("w") as f:
            json.dump(result_data, f, indent=4)

        print(f"Detection completed. Results saved to '{result_file.absolute()}'.")
