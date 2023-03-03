# photo-location-finder
This is a Python code to detect landmarks, labels and web entities in a set of images using Google Cloud Vision API. The code takes a JSON configuration file that contains the API key and credentials file path for the Google Cloud Vision API, as well as other optional parameters, such as the directory for image files.

The code processes each image file and extracts landmark, label, and web entity information from it using the aforementioned API. The results are stored in a JSON file in the following structure:

# Prerequisites

Before running the program, the user needs to have:

* A valid Google Cloud API key
* Google Cloud credentials file
* A Directory with Images for landmark detection
    
# Installation

Clone the repository into your local machine.

```git clone https://github.com/your_username/image-recog.git```

Download Google Cloud Vision API Client Library [https://cloud.google.com/vision/docs/libraries?hl=de#client-libraries-install-python] for Python using pip:

```pip install google-cloud-vision```

Install dependencies listed in requirements.txt by running:

```pip install -r requirements.txt```

Set up a Google Cloud Platform account by following the instructions given in official documentation [https://cloud.google.com/vision/docs/before-you-begin?hl=de]

Follow the instructions mentioned on this page to obtain an API key, create a project and enable billing feature.

 {
     "google_cloud_api_key": "AIzaSyAc97pD-Yrixrkx2ZDWV6KdHsUo2TjA2r8",
     "google_application_credentials_file_path": "./google-creds.json",
     "image_directory_path": "./images"
  }
  
Update the values in the JSON configuration file that store the API key, credentials file path, and other parameters matching your own GCP account details.
Store images you want to analyse in the directory mentioned in JSON file.

# Usage

To use the program, open command prompt and simply navigate in your directory where the file is located with cd C:\Users\Name\Downloads and then run the photolocationfinder.py in your command prompt. The program will prompt the user to enter the config.json file path. 

Follow the prompt that appears to enter the path to your JSON configuration file when prompted.

Wait for the process to complete, then check for the output file 'result.json', which has the detected landmarks, labels and web entities.

# License

This program is licensed under the MIT License. See the LICENSE file for more information.

# Contact

For any questions or suggestions, please contact the author via the Issues or Pull requests.
