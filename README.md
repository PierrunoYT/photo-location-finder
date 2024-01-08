# photo-location-finder

This Python program detects landmarks, labels, and web entities in a set of images using the Google Cloud Vision API. The program takes a JSON configuration file that contains the API key and credentials file path for the Google Cloud Vision API, as well as other optional parameters, such as the directory for image files.

## Prerequisites

Before running the program, ensure that you have:

- A valid Google Cloud API key
- Google Cloud credentials file
- A directory with images for landmark detection
- All required libraries and packages

## Installation

1. Clone the repository onto your local machine:
   ```
   git clone https://github.com/PierrunoYT/photo-location-finder
   ```
   Alternatively, download the zip file from GitHub.

2. Ensure that you have Python 3.7 or later installed on your local machine.

3. Navigate to the root directory of the project and install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Obtain API keys for Google Cloud Vision API and Google Maps API by following the documentation provided by each respective API.

5. Set up the authentication credentials for Google Cloud Vision API by creating a service account and storing the private key JSON file in a secure location. Follow the instructions provided in the [Google Cloud Vision Official Documentation](https://cloud.google.com/vision/docs/before-you-begin)

6. Open the `config.json` file and replace the placeholders with your actual Google Maps API key and the path to the private key JSON file. Update other parameters in the configuration file if necessary.

7. Store the images you want to analyze in the directory mentioned in the `image_dir` parameter specified in the `config.json` file.

8. To run the script, navigate to the root directory of the project and run the following command:
   ```
   python main.py
   ```
   The detection process will start, and you will see output in the terminal indicating the status of each image being processed. When the process is complete, you will find a `result.json` file in the current working directory containing the results of the object detection.

## License

This program is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact

For any questions or suggestions, please contact the author via the Issues or Pull requests.
