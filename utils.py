import os
import cv2
import soundfile as sf

# Define the audio sample rate (Hz)
sample_rate = 16000  # Adjust this value based on your requirements

# Define a function to merge the transcriptions from multiple parts
def merge_transcriptions(output_file):
    with open(output_file, "r") as f:
        transcriptions = f.read().split()
    return " ".join(transcriptions)

# Define a function to split the video into audio parts
def split_video(video_path, output_directory, silence_threshold):
    cap = cv2.VideoCapture(video_path)
    os.makedirs(output_directory, exist_ok=True)

    audio_segments = []
    silence_detected = False
    part_number = 1

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
            # Save the audio segment as a WAV file
            audio_path = os.path.join(output_directory, f"part_{part_number}.wav")
            sf.write(audio_path, audio_segments[:-1], sample_rate)

            # Clear the processed audio segments
            audio_segments = [audio_segments[-1]]
            silence_detected = False
            part_number += 1

    # Save the final audio segment as a WAV file
    audio_path = os.path.join(output_directory, f"part_{part_number}.wav")
    sf.write(audio_path, audio_segments, sample_rate)

    # Release the video capture
    cap.release()