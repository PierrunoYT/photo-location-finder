# 📸 Photo Location Finder

Welcome to the **Photo Location Finder** project repository! This tool is designed to help you extract and identify the geographical location of the photos using EXIF data, Google Vision API, and Google Maps API.

---

## 🌟 Features

- **EXIF Data Extraction**: Extracts GPS coordinates from image metadata.
- **Google Vision API Integration**: Detects landmarks, labels, web entities, and more from images.
- **Reverse Geocoding**: Converts GPS coordinates into human-readable addresses using Google Maps API.
- **Street View**: Provides a street view image of the location.
- **Web Interface**: Allows users to upload and process images via a simple web interface.

---

## 📖 Introduction

The Photo Location Finder is a Python-based application that leverages Google Cloud's Vision API to analyze images and extract location-based information. It is particularly useful for photographers, travelers, and researchers who need to organize or verify the locations where pictures were taken.

---

## 📋 Requirements

To run this project, ensure you have the following software and libraries installed:

- Python 3.8 or higher
- Google Cloud Vision API credentials
- Required Python packages (see below for installation)

**Python Packages**:
- `google-auth==2.18.0`
- `google-auth-oauthlib==0.4.2`
- `google-auth-httplib2==0.1.0`
- `google-api-python-client==2.86.0`
- `google-cloud-vision==3.7.2`
- `aiohttp==3.8.4`
- `tenacity==8.2.2`
- `Pillow==9.5.0`
- `Flask==2.3.2`

---

## ⚙️ Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/PierrunoYT/photo-location-finder.git
   cd photo-location-finder
   ```

2. **Set up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Use the following command to install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google API Credentials**

   a. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   b. Enable the Vision API and Maps API for your project.
   c. Create API credentials (API key and service account key).
   d. Create a `config.json` file based on `config.json.template` and fill in your Google API credentials and other configurations.

   ```json
   {
     "google_api_key": "YOUR_GOOGLE_API_KEY_HERE",
     "google_application_credentials_file_path": "PATH_TO_YOUR_GOOGLE_APPLICATION_CREDENTIALS_FILE",
     "image_directory_path": "PATH_TO_YOUR_IMAGE_DIRECTORY"
   }
   ```

5. **Set up the Upload Directory**

   Create a directory named `uploads` in the project root:

   ```bash
   mkdir uploads
   ```

6. **Run the Application**

   ```bash
   python web_app.py
   ```

   The application will be available at `http://localhost:5000`.

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## 🤝 Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

---

## 🔧 Configuration

Ensure your `config.json` is set up with the correct paths and API keys. The template is as follows:

```json
{
  "google_api_key": "YOUR_GOOGLE_API_KEY_HERE",
  "google_application_credentials_file_path": "PATH_TO_YOUR_GOOGLE_APPLICATION_CREDENTIALS_FILE",
  "image_directory_path": "PATH_TO_YOUR_IMAGE_DIRECTORY"
}
```

---

## 🚀 Usage

1. **Start the Web Application**

   Run the following command to start the Flask web application:

   ```bash
   python web_app.py
   ```

2. **Upload Images**

   Navigate to `http://localhost:5000` in your web browser. Use the web interface to upload images and view the extracted location details.

---

Thank you for using the Photo Location Finder! If you encounter any issues or have suggestions, feel free to create an issue or reach out. Happy exploring! 📷🌍
