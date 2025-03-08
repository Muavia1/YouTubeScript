# YouTubeScript 🎙️

##  Project Description
YouTubeScript is a simple and efficient application that allows users to transcribe YouTube videos or uploaded audio files into text. It supports both original language transcription and language translation with subtitle files in `.vtt` format.

##  Features
-  Transcribe YouTube videos via URL
-  Transcribe uploaded audio files
-  Translate transcriptions to multiple languages
-  Generate `.vtt` subtitle files
-  Summarize transcriptions using a language model
-  Easy interface with clear fields for repeated use

##  Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/YouTubeScript.git
cd YouTubeScript
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Install ffmpeg** (Required for Whisper)
- Linux: `sudo apt install ffmpeg`
- Windows: [Download here](https://ffmpeg.org/download.html)

##  Required Packages
- `gradio`
- `openai-whisper`
- `transformers`
- `yt-dlp`

##  Usage

Run the application with:
```bash
python app.py
```

##  How to Use
1. Select input type: YouTube video or audio file.
2. Provide the YouTube link or upload an audio file.
3. Choose the mode: Original or Translate.
4. Select a language if translating.
5. Click **Get YouTubeScript 🪄**.
6. View the transcription summary and download the `.vtt` file.
7. Click **Clear Fields ** to reset the interface.

##  Project Structure
```bash
.
├── app.py        # Main application code
├── requirements.txt # Dependency file
├── README.md     # Project documentation
└── sub.vtt       # Generated subtitle file
```

##  Sample Commands
- To transcribe a YouTube video:
  - Provide the URL and click **Get YouTubeScript 🪄**.
- To transcribe an uploaded file:
  - Upload an audio file and follow the same steps.

## ⚠ Troubleshooting
- **No transcription or empty subtitles**: Make sure `ffmpeg` is installed.
- **Failed YouTube download**: Confirm `yt-dlp` installation.



Happy Transcribing! 
