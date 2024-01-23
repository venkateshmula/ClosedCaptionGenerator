import cv2
import concurrent.futures
from utils import split_video, merge_transcriptions
from transcription import transcribe_audio

# Load the video using OpenCV
video_path = "path/to/your/video.mp4"
cap = cv2.VideoCapture(video_path)

# Define the number of workers for parallel processing
num_workers = 4  # Modify this value based on your system's capabilities

# Define the silence threshold for splitting the video
silence_threshold = -40  # Adjust this value based on your video's audio characteristics

# Define the output file for the closed captions
output_file = "path/to/output/captions.txt"

# Process each frame of the video
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    audio_segments = []
    silence_detected = False

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Preprocess the audio of the frame
        audio = frame.mean(axis=2)

        # Check if the audio frame is silent
        if audio.mean() < silence_threshold:
            silence_detected = True

        # Accumulate audio segments
        audio_segments.append(audio)

        # Split the video if a silence is detected
        if silence_detected and len(audio_segments) > 1:
            # Transcribe each audio segment in parallel
            futures = []
            for segment in audio_segments[:-1]:
                future = executor.submit(transcribe_audio, segment)
                futures.append(future)

            # Wait for all the transcriptions to complete
            transcriptions = [future.result() for future in futures]

            # Write the transcriptions to the output file
            with open(output_file, "a") as f:
                f.write(" ".join(transcriptions) + " ")

            # Clear the processed audio segments
            audio_segments = [audio_segments[-1]]
            silence_detected = False

# Release the video capture
cap.release()

# Perform any final transcription on remaining audio segments, if any
if len(audio_segments) > 0:
    transcriptions = [transcribe_audio(segment) for segment in audio_segments]

    # Write the final transcriptions to the output file
    with open(output_file, "a") as f:
        f.write(" ".join(transcriptions) + " ")

# Finish and provide the output file path
print(f"Closed captions file: {output_file}")

# Merge the transcriptions from multiple parts
merged_transcriptions = merge_transcriptions(output_file)

# Print the merged transcriptions
print("Merged Transcriptions:")
print(merged_transcriptions)