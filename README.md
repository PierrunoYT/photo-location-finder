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

1. To clone the repository onto your local machine, open a terminal or command prompt and enter the following command:

```git clone https://github.com/PierrunoYT/photo-location-finder```

Alternatively, you can download the zip file from GitHub by clicking on the green "Code" button and selecting "Download ZIP".

2. To ensure that you have Python 3.7 or later installed on your local machine, enter the following command in your terminal or command prompt:

  ``` python --version```

If you don't have Python 3.7 or later installed, you can download it from the official Python website.

3. Next, navigate to the root directory of the project where the requirements.txt file is located, and run the following command to install all the required packages:

```pip install -r requirements.txt```

4. Obtain API keys for Google Cloud Vision API and Google Maps API by following the documentation provided by each respective API.

5. Set up the authentication credentials for Google Cloud Vision API by creating a service account and storing the private key JSON file in a secure location. Follow the instructions provided in the [Google Cloud Vision Official Documentation](https://cloud.google.com/vision/docs/before-you-begin)

After setting up the credentials, create a new file named config.json in the root directory of the project. Copy the contents of config.sample.json into config.json, and replace the YOUR_API_KEY_HERE placeholder with your actual Google Maps API key, and the PATH_TO_YOUR_CREDENTIALS_FILE placeholder with the path to the private key JSON file you created earlier. Update other parameters in the configuration file if necessary.

5. Store the images you want to analyze in the directory mentioned in the image_dir parameter specified in the config.json file.

6. To run the script, navigate to the root directory of the project in your terminal or command prompt, and type in the following command:

```python main.py```

The detection process will start, and you will see output in the terminal or command prompt indicating the status of each image being processed. 
When the process is complete, you will find a result.json file in the current working directory containing the results of the object detection.

# License

This program is licensed under the MIT License. See the LICENSE file for more information.

# Contact

For any questions or suggestions, please contact the author via the Issues or Pull requests.
