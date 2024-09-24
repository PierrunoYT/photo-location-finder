# 📸 Photo Location Finder

## 📖 Introduction

Photo Location Finder is a Python-based application that extracts and identifies the geographical location of photos using EXIF data, Google Vision API, and Google Maps API. It's designed for photographers, travelers, and researchers who need to organize or verify the locations where pictures were taken.

## 🌟 Features

- EXIF Data Extraction: Extracts GPS coordinates from image metadata
- Google Vision API Integration: Detects landmarks, labels, web entities, and more
- Reverse Geocoding: Converts GPS coordinates into human-readable addresses
- Street View: Provides a street view image of the location
- Web Interface: Allows users to upload and process images via a simple web interface

## 📋 Requirements

- Python 3.8 or higher
- Google Cloud Vision API credentials
- Required Python packages (listed in `requirements.txt`)

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PierrunoYT/photo-location-finder.git
   cd photo-location-finder
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Google API Credentials:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Vision API and Maps API for your project
   - Create API credentials (API key and service account key)
   - Create a `config.json` file based on `config.json.template`

5. Set up the upload directory:
   ```bash
   mkdir uploads
   ```

## 🔧 Configuration

Ensure your `config.json` is set up with the correct paths and API keys:

```json
{
  "google_api_key": "YOUR_GOOGLE_API_KEY_HERE",
  "google_application_credentials_file_path": "PATH_TO_YOUR_GOOGLE_APPLICATION_CREDENTIALS_FILE",
  "image_directory_path": "PATH_TO_YOUR_IMAGE_DIRECTORY"
}
```

## 🚀 Usage

1. Start the web application:
   ```bash
   python web_app.py
   ```

2. Open `http://localhost:5000` in your web browser

3. Upload images and view the extracted location details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Support

If you encounter any issues or have suggestions, please create an issue in the GitHub repository.

Happy exploring! 📷🌍
