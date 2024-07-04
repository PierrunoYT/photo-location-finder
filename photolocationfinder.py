import asyncio
import os
import json
from pathlib import Path
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import aiohttp
from google.cloud import vision_v1
from google.cloud.vision_v1.types import Feature
from tenacity import retry, stop_after_attempt, wait_exponential

class ImageProcessor:
    def __init__(self, api_key, cred_path, image_dir, prompt_for_confirmation):
        self.api_key = api_key
        self.cred_path = cred_path
        self.image_dir = image_dir
        self.prompt_for_confirmation = prompt_for_confirmation
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.cred_path
        self.client = None

    def initialize_client(self):
        if self.client is None:
            self.client = vision_v1.ImageAnnotatorClient()

    async def initialize_client_async(self):
        if self.client is None:
            self.client = vision_v1.ImageAnnotatorClient()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def process_image(self, image_path: str):
        """Processes a single image using the given client."""
        try:
            with open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision_v1.Image(content=content)
            features = [
                Feature(type=Feature.Type.LANDMARK_DETECTION),
                Feature(type=Feature.Type.LABEL_DETECTION),
                Feature(type=Feature.Type.WEB_DETECTION),
                Feature(type=Feature.Type.IMAGE_PROPERTIES),
                Feature(type=Feature.Type.SAFE_SEARCH_DETECTION)
            ]
            response = self.client.annotate_image({
                'image': image,
                'features': features,
            })

            if response.error.message:
                raise Exception(f"[VISION API ERROR] - {response.error.message}")

            result_data = {
                "filename": image_path,
                "landmarks": [],
                "labels": [],
                "web_entities": [],
                "dominant_colors": [],
                "safe_search": {}
            }

            # Try to get GPS data from EXIF
            gps_info = self.get_gps_from_exif(image_path)
            if gps_info:
                result_data["gps_location"] = gps_info
                print(f"[INFO]: GPS data found in EXIF for '{image_path}'")
            else:
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
                    result_data["labels"].append({"label": label.description, "score": label.score})

            web_entities = response.web_detection.web_entities
            if web_entities:
                for entity in web_entities:
                    result_data["web_entities"].append({"entity": entity.description, "score": entity.score})

            # Add dominant colors
            colors = response.image_properties_annotation.dominant_colors.colors
            for color in colors[:5]:  # Get top 5 dominant colors
                result_data["dominant_colors"].append({
                    "red": color.color.red,
                    "green": color.color.green,
                    "blue": color.color.blue,
                    "score": color.score,
                    "pixel_fraction": color.pixel_fraction
                })

            # Add safe search annotation
            safe_search = response.safe_search_annotation
            result_data["safe_search"] = {
                "adult": safe_search.adult,
                "medical": safe_search.medical,
                "spoofed": safe_search.spoof,
                "violence": safe_search.violence,
                "racy": safe_search.racy
            }

            print(f"[INFO]: Successfully processed image '{image_path}'")
            await self.save_intermediate_result(result_data)
            return result_data

        except FileNotFoundError as f:
            raise Exception(f"[IO ERROR][Image '{image_path}']: {f}") from f
        except Exception as e:
            raise Exception(f"[PROCESSING ERROR][Image '{image_path}']: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    async def save_intermediate_result(self, result_data):
        """Saves intermediate results to a JSON file."""
        intermediate_file = Path(f'intermediate_results_{int(time.time())}.json')
        with intermediate_file.open("w") as f:
            json.dump(result_data, f, indent=4)
        print(f"Intermediate result saved to '{intermediate_file.absolute()}'.")

    def get_gps_from_exif(self, image_path):
        """Extracts GPS coordinates from image EXIF data if available."""
        try:
            with Image.open(image_path) as img:
                exif = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
                if 'GPSInfo' in exif:
                    gps_info = {GPSTAGS[k]: v for k, v in exif['GPSInfo'].items() if k in GPSTAGS}
                    lat = gps_info['GPSLatitude']
                    lon = gps_info['GPSLongitude']
                    lat_ref = gps_info['GPSLatitudeRef']
                    lon_ref = gps_info['GPSLongitudeRef']
                    
                    lat = (lat[0] + lat[1]/60 + lat[2]/3600) * (-1 if lat_ref == 'S' else 1)
                    lon = (lon[0] + lon[1]/60 + lon[2]/3600) * (-1 if lon_ref == 'W' else 1)
                    
                    return {"latitude": lat, "longitude": lon}
        except Exception as e:
            print(f"Error extracting EXIF data from {image_path}: {e}")
        return None

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

    def process_single_image(self, image_path):
        """Processes a single image and returns the result."""
        self.initialize_client()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.process_image(image_path))
        loop.close()
        return result
