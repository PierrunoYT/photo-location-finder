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

Open your terminal or command prompt and navigate to the directory where you cloned the repository using the cd command. 

Once you are in the project directory, run the following command to start the program:

```python photolocationfinder.py

The program will ask you to provide the name of the image file that you want to analyze. Enter the name of the file (including the file extension like .jpg, .png, etc.) and press enter.

The program will then use the Google Cloud Vision API to analyze the image and extract information such as labels, landmarks, and location data.

After analyzing the image, the program will display the results on the console.

# License

This program is licensed under the MIT License. See the LICENSE file for more information.

# Contact

For any questions or suggestions, please contact the author via the Issues or Pull requests.
