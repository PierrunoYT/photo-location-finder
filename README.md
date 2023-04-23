# photo-location-finder
This is a Python code to detect landmarks, labels and web entities in a set of images using Google Cloud Vision API. The code takes a JSON configuration file that contains the API key and credentials file path for the Google Cloud Vision API, as well as other optional parameters, such as the directory for image files.

The code processes each image file and extracts landmark, label, and web entity information from it using the aforementioned API. The results are stored in a JSON file in the following structure:

# Prerequisites

Before running the program, the user needs to have:

* A valid Google Cloud API key
* Google Cloud credentials file
* A Directory with Images for landmark detection
* All required libraries and packages
    
# Installation

Clone the repository onto your local machine using Git clone command or download the zip file from GitHub:

```git clone https://github.com/PierrunoYT/photo-location-finder```

Make sure you have Python 3.7 or later installed on your local machine. You can check this by running python --version in your terminal or command prompt.

```pip install -r requirements.txt```

Note: Make sure to run this command in the root directory of the project where the requirements.txt file is located.

Obtain API keys for Google Cloud Vision API and Google Maps API. Please follow the documentation of respective APIs to acquire the keys.

Set up the authentication credentials for Google Cloud Vision API by creating a service account and storing the private key JSON file in a secure location. Please follow the instructions provided in the [Google Cloud Vision Official Documentation](https://cloud.google.com/vision/docs/before-you-begin)

Once you have obtained the API keys and set up the Google Cloud Vision credentials, create a new file named config.json in the root directory of the project. Copy the contents of config.sample.json into config.json and replace YOUR_API_KEY_HERE with your actual Google Maps API key and PATH_TO_YOUR_CREDENTIALS_FILE with the path to the JSON credentials file you created earlier. You can also update other parameters in the configuration file if required.

Store images you want to analyze in the directory mentioned in the JSON file (image_dir parameter).

Run the script using the following command in your terminal or command prompt:

```python main.py```

The detection process will start, and you will see output in your terminal or command prompt indicating the status of each image being processed.

When the process is complete, you will find a result.json file in the current working directory containing the results of the object detection.

# License

This program is licensed under the MIT License. See the LICENSE file for more information.

# Contact

For any questions or suggestions, please contact the author via the Issues or Pull requests.
