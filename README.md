# photo-location-finder

This Python program detects landmarks, labels, web entities, and other image properties in a set of images using the Google Cloud Vision API. The program takes a JSON configuration file that contains the API key and credentials file path for the Google Cloud Vision API, as well as other optional parameters, such as the directory for image files.

## Features

- Landmark detection
- Label detection
- Web entity detection
- Image properties analysis (dominant colors)
- Safe search detection
- Asynchronous processing for improved performance
- Error handling and retries for API calls
- Intermediate results saving
- GPS data extraction from EXIF metadata
- Geolocation using Google Maps API when landmark detection fails

## Prerequisites

Before running the program, ensure that you have:

- A valid Google Cloud API key
- Google Cloud credentials file
- Google Maps API key
- A directory with images for analysis
- Python 3.7 or later
- All required libraries and packages

## Installation

1. Clone the repository onto your local machine:
   ```
   git clone https://github.com/PierrunoYT/photo-location-finder
   ```
   Alternatively, download the zip file from GitHub.

2. Navigate to the root directory of the project and install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Obtain API keys for Google Cloud Vision API and Google Maps API by following the documentation provided by each respective API.

4. Set up the authentication credentials for Google Cloud Vision API by creating a service account and storing the private key JSON file in a secure location. Follow the instructions provided in the [Google Cloud Vision Official Documentation](https://cloud.google.com/vision/docs/before-you-begin)

5. Open the `config.json` file and replace the placeholders with your actual Google Maps API key, the path to the private key JSON file, and the directory path for your images. Update other parameters in the configuration file if necessary.

## Usage

1. Ensure your images are stored in the directory specified in the `image_directory_path` parameter in `config.json`.

2. To run the script, navigate to the root directory of the project and run the following command:
   ```
   python main.py
   ```

3. The detection process will start, and you will see output in the terminal indicating the status of each image being processed. 

4. When the process is complete, you will find:
   - A `result.json` file in the current working directory containing the final results of the image analysis.
   - Multiple `intermediate_results_[timestamp].json` files containing intermediate results for each processed image.

## Error Handling and Retries

The program implements error handling and retries for API calls using the `tenacity` library. If an API call fails, it will be retried up to 3 times with exponential backoff.

## License

This program is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact

For any questions, suggestions, or issues, please open an issue on the GitHub repository or submit a pull request.
