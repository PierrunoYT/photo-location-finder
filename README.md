# photo-location-finder
This is a Python code to detect landmarks, labels and web entities in a set of images using Google Cloud Vision API. The code takes a JSON configuration file that contains the API key and credentials file path for the Google Cloud Vision API, as well as other optional parameters, such as the directory for image files.

The code processes each image file and extracts landmark, label, and web entity information from it using the aforementioned API. The results are stored in a JSON file in the following structure:

# Prerequisites

Before running the program, the user needs to have:

* A valid Google Cloud API key
* Google Cloud credentials file
* A Directory with Images for landmark detection
    
# Installation

Clone the repository into your local machine using the following command:

```git clone https://github.com/PierrunoYT/photo-location-finder```

Download Google [Cloud Vision API Client Library](https://cloud.google.com/vision/docs/libraries?hl=de#client-libraries-install-python) and the other package for Python using pip:

```pip install aiohttp google-cloud-vision```

This will install the aiohttp and google-cloud-vision packages which are required for the project.

Install dependencies listed in requirements.txt by running:

```pip install -r requirements.txt```

This command will install all the required dependencies mentioned in the requirements.txt file.

Set up a Google Cloud Platform account by following the instructions given in official [documentation](https://cloud.google.com/vision/docs/before-you-begin?hl=de)

Follow the instructions mentioned on this page to obtain an API key, create a project and enable billing feature.
  
Update the values in the JSON configuration file (config.json) that store the API key, credentials file path, and other parameters matching your own GCP account details.

Store images you want to analyze in the directory mentioned in the JSON file.

# Usage

To use the program, open command prompt and simply navigate in your directory where the file is located with cd C:\Users\Name\Downloads and then run the photolocationfinder.py in your command prompt. The program will prompt the user to enter the config.json file path. 

Follow the prompt that appears to enter the path to your JSON configuration file when prompted.

Wait for the process to complete, then check for the output file 'result.json', which has the detected landmarks, labels and web entities.

# License

This program is licensed under the MIT License. See the LICENSE file for more information.

# Contact

For any questions or suggestions, please contact the author via the Issues or Pull requests.
