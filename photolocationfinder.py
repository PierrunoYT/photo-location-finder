import asyncio
import os
import json
from pathlib import Path
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import aiohttp
from google.cloud import vision
from google.cloud.vision_v1 import types
from tenacity import retry, stop_after_attempt, wait_exponential
from urllib.parse import quote

class ImageProcessor:
    def __init__(self, api_key, cred_path, image_dir, prompt_for_confirmation):
        self.api_key = api_key
        self.cred_path = cred_path
        self.image_dir = image_dir
        self.prompt_for_confirmation = prompt_for_confirmation
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.cred_path
        self.client = None
        self.session = None

    async def initialize(self):
        if self.client is None:
            self.client = vision.ImageAnnotatorClient()
        if self.session is None:
            self.session = aiohttp.ClientSession()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def process_image(self, image_path: str):
        try:
            print(f"Processing image: {image_path}")
            with open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            features = [
                types.Feature(type=types.Feature.Type.LANDMARK_DETECTION),
                types.Feature(type=types.Feature.Type.LABEL_DETECTION),
                types.Feature(type=types.Feature.Type.WEB_DETECTION),
                types.Feature(type=types.Feature.Type.IMAGE_PROPERTIES),
                types.Feature(type=types.Feature.Type.SAFE_SEARCH_DETECTION),
                types.Feature(type=types.Feature.Type.DOCUMENT_TEXT_DETECTION)
            ]

            request = types.AnnotateImageRequest(image=image, features=features)
            print("Sending request to Google Vision API...")
            response = self.client.annotate_image(request=request)
            print("Received response from Google Vision API")

            if response.error.message:
                raise Exception(f"[VISION API ERROR] - {response.error.message}")

            print("Extracting data from response...")
            result_data = self.extract_data_from_response(response, image_path)
            print("Data extraction complete")

            print("Extracting text coordinates...")
            text_coordinates = self.extract_text_coordinates(response)
            result_data["text_coordinates"] = text_coordinates
            print("Text coordinate extraction complete")

            print("Checking for GPS data in EXIF...")
            gps_info = self.get_gps_from_exif(image_path)
            if gps_info:
                print(f"GPS data found: {gps_info}")
                result_data["gps_location"] = gps_info
                print("Reverse geocoding GPS coordinates...")
                address = await self.reverse_geocode(gps_info["latitude"], gps_info["longitude"])
                if address:
                    print(f"Address found: {address}")
                    result_data["address"] = address
            elif not result_data.get("landmarks"):
                print("No GPS data or landmarks found. Attempting to get location from text...")
                location = await self.get_location_from_text(text_coordinates)
                if location:
                    print(f"Location found from text: {location}")
                    result_data["location"] = location
                    print("Reverse geocoding location...")
                    address = await self.reverse_geocode(location["lat"], location["lng"])
                    if address:
                        print(f"Address found: {address}")
                        result_data["address"] = address
                else:
                    print("No location found from text. Attempting to get location from Google Maps API...")
                    location = await self.get_location_from_google_maps_api(result_data["labels"][:3])
                    if location:
                        print(f"Location found from Google Maps API: {location}")
                        result_data["location"] = location
                        print("Reverse geocoding location...")
                        address = await self.reverse_geocode(location["lat"], location["lng"])
                        if address:
                            print(f"Address found: {address}")
                            result_data["address"] = address
                    else:
                        print("No location found from Google Maps API")
            else:
                print(f"Landmarks found: {result_data['landmarks']}")

            print("Saving intermediate result...")
            await self.save_intermediate_result(result_data)
            print("Processing complete")
            return result_data

        except Exception as e:
            print(f"[PROCESSING ERROR][Image '{image_path}']: {str(e)}")
            return {"error": str(e), "filename": image_path}

    async def get_location_from_text(self, text_coordinates):
        location_text = " ".join([item["text"] for item in text_coordinates])
        return await self.get_location_from_google_maps_api([{"label": location_text}])

    def extract_data_from_response(self, response, image_path):
        result_data = {
            "filename": image_path,
            "landmarks": [],
            "labels": [],
            "web_entities": [],
            "dominant_colors": [],
            "safe_search": {}
        }

        if response.landmark_annotations:
            for landmark in response.landmark_annotations:
                if landmark.locations and landmark.locations[0].lat_lng:
                    result_data["landmarks"].append({
                        "name": landmark.description,
                        "latitude": landmark.locations[0].lat_lng.latitude,
                        "longitude": landmark.locations[0].lat_lng.longitude,
                        "confidence": landmark.score
                    })
            if result_data["landmarks"]:
                result_data["location"] = {
                    "lat": result_data["landmarks"][0]["latitude"],
                    "lng": result_data["landmarks"][0]["longitude"]
                }

        result_data["labels"] = [{"label": label.description, "score": label.score} for label in response.label_annotations]
        result_data["web_entities"] = [{"entity": entity.description, "score": entity.score} for entity in response.web_detection.web_entities]

        colors = response.image_properties_annotation.dominant_colors.colors
        result_data["dominant_colors"] = [{
            "red": color.color.red,
            "green": color.color.green,
            "blue": color.color.blue,
            "score": color.score,
            "pixel_fraction": color.pixel_fraction
        } for color in colors[:5]]

        safe_search = response.safe_search_annotation
        result_data["safe_search"] = {
            "adult": safe_search.adult,
            "medical": safe_search.medical,
            "spoofed": safe_search.spoof,
            "violence": safe_search.violence,
            "racy": safe_search.racy
        }

        return result_data

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_location_from_google_maps_api(self, object_labels: list[str]):
        query = " ".join(label["label"] for label in object_labels)
        encoded_query = quote(query)
        url = f"https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.types"
        }
        data = json.dumps({"textQuery": encoded_query})
        async with self.session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("places"):
                    place = data["places"][0]
                    return {
                        "lat": place["location"]["latitude"],
                        "lng": place["location"]["longitude"],
                        "name": place["displayName"]["text"],
                        "address": place["formattedAddress"],
                        "types": place.get("types", [])
                    }
        return None

    async def get_location_from_text(self, text_coordinates):
        location_text = " ".join([item["text"] for item in text_coordinates])
        return await self.get_location_from_google_maps_api([{"label": location_text}])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def reverse_geocode(self, lat: float, lng: float):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={self.api_key}"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["status"] == "OK" and data["results"]:
                    result = data["results"][0]
                    return {
                        "address": result["formatted_address"],
                        "types": result["types"],
                        "place_id": result["place_id"]
                    }
        return None

    def get_files_by_extension(self, extensions: list[str]):
        return [f for ext in extensions for f in Path(self.image_dir).glob(f"*.{ext}")]

    async def save_intermediate_result(self, result_data):
        intermediate_file = Path(f'intermediate_results_{int(time.time())}.json')
        with intermediate_file.open("w") as f:
            json.dump(result_data, f, indent=4)
        print(f"Intermediate result saved to '{intermediate_file.absolute()}'.")

    def get_gps_from_exif(self, image_path):
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

    def extract_text_coordinates(self, response):
        coordinates = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        box = word.bounding_box
                        coords = [(vertex.x, vertex.y) for vertex in box.vertices]
                        coordinates.append({
                            'text': ''.join([symbol.text for symbol in word.symbols]),
                            'coords': coords
                        })
        return coordinates

    async def process_images(self):
        await self.initialize()
        image_files = self.get_files_by_extension(["png", "jpg", "jpeg"])
        num_images = len(image_files)
        if num_images == 0:
            print("No images found in the specified directory.")
            return

        print(f"{num_images} image files found.")

        if num_images > 100 and self.prompt_for_confirmation:
            confirm = input(f"WARNING: {num_images} images found. Continue? (y/n): ")
            if not confirm.lower().startswith("y"):
                print("Operation cancelled.")
                return

        tasks = [self.process_image(str(img_f)) for img_f in image_files]
        results = await asyncio.gather(*tasks)

        result_file = Path('result.json')
        with result_file.open("w") as f:
            json.dump(results, f, indent=4)

        print(f"Processing completed. Results saved to '{result_file.absolute()}'.")
        await self.session.close()

    def process_single_image(self, image_path):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._process_single_image(image_path))
        finally:
            loop.close()

    async def _process_single_image(self, image_path):
        await self.initialize()
        result = await self.process_image(image_path)
        await self.session.close()
        return result

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    processor = ImageProcessor(
        api_key=config['google_api_key'],
        cred_path=config['google_application_credentials_file_path'],
        image_dir=config['image_directory_path'],
        prompt_for_confirmation=True
    )
    
    asyncio.run(processor.process_images())
