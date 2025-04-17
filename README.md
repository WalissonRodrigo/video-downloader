# Video Downloader

A simple command-line tool to download videos from various platforms using yt-dlp.

## Features

- Download videos from YouTube and other supported platforms
- Select video quality (best, 720p, 480p, 360p)
- Track download history
- Progress bar for downloads
- Colorful terminal interface
- Multi-language support (English and Portuguese)

## Requirements

- Python 3.6+
- pip (Python package manager)

## Installation

1. Clone or download this repository:

```bash
git clone https://github.com/WalissonRodrigo/video-downloader.git
cd video-downloader
```

2. Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

if have problem with the installation of the requirements.txt, try to install the requirements one by one:

```bash
python -m pip install yt-dlp tqdm colorama
```

## Usage

To use the video downloader, run the following command:

```bash
python downloader.py
```

### Main Menu Options

The program presents a simple menu with the following options:

1. Download Video : Enter a URL and select quality to download a video
2. View Download History : See a list of previously downloaded videos
3. Clear History : Remove all entries from the download history
4. Change Language : Switch between English and Portuguese
5. Exit : Close the application

### Downloading Videos

When downloading a video:

1. Enter the URL when prompted
2. Select the desired quality:
   - Option 1: Best quality
   - Option 2: 720p
   - Option 3: 480p
   - Option 4: 360p
     The video will be downloaded to the Downloads/VideoDownloader folder in your user directory.

### Changing Language

The application supports both English and Portuguese:

1. Select "Change Language" from the main menu
2. Choose your preferred language:
   - Option 1: English
   - Option 2: Portuguese
Your language preference will be saved for future sessions.

## Supported Platforms

This tool supports all platforms that yt-dlp can handle, including:

- YouTube
- Vimeo
- Facebook
- Twitter
- Instagram
- And many more

## Troubleshooting

If you encounter any issues:

- Make sure you have the latest version of yt-dlp installed
- Check that the URL is valid and accessible
- Verify that you have a stable internet connection
- Ensure you have sufficient disk space for the download

## License

This README provides clear instructions on how to install and use your video downloader application.
It covers the main features, installation steps, usage instructions, and basic troubleshooting tips.
