# ClosedCaptionGenerator
# Audio Transcription Project

This project allows you to transcribe broken audio parts in parallel from a video and combine the final transcripts into a single output file.

## Prerequisites

- Python 3.6 or above
- pip package manager

## Installation

1. Clone this repository to your local machine or download the source code as a ZIP file.

2. Open a terminal or command prompt and navigate to the project directory.

3. Install the required Python packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```


  ## Usage
1. Place your video file in the project directory.
2. Open the main.py file and modify the following variables according to your requirements:
   video_path: Path to your video file.
   num_workers: Number of workers for parallel processing (adjust based on your system's capabilities).
   silence_threshold: Silence threshold for splitting the video (adjust based on your video's audio characteristics).
   output_file: Path to the output file for closed captions.
3. Run the code by executing the following command:
   
```
python main.py
```

After the code finishes execution, you will find the closed captions saved in the specified output_file.

## Advanced Usage
If you want to customize the behavior further, you can modify the code in the respective files:
transcription.py: Contains the audio transcription logic.
utils.py: Includes utility functions for file handling and video splitting.
Feel free to explore the code and adapt it to your specific requirements.
