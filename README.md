## Documentation

Detailed documentation about the usage of the library can be found at [hindi-dataset.io](https://pytube.io). This is recommended for most cases.

## Description 

### YouTube Video to Audio Converter for Speech Recognition

This project aims to create a system that can retrieve YouTube videos based on a user query and convert them into audio files that are suitable for speech recognition. The system can be useful for applications such as speech-to-text transcription, voice search, voice assistant, and voice analysis.

## Requirements

The system requires the following Python libraries:

- request: To get the video IDs of the relevant videos for the user query using the YouTube Data API.
- pytube: To download the audio of the videos
- youtube_transcript_api: To get the transcript of the videos using the YouTube Transcript API.
- whisper: To detect the language of the audio.
- pydub: To segment the audio files based on the transcript.
- spleeter: To extract the vocals from the audio files using a source separation library.
- librosa: To resample the audio files to a common frame rate, sample width, and number of channels using an audio analysis library.

## Usage

To use the system, follow these steps:

1. Clone this repository to your local machine.
2. Install the required libraries using `poetry install`
3. Run `streamlit run home.py` and enter your user query when prompted.
4. The system will retrieve the video IDs of the relevant videos for your query and will filter out the video IDs that do not have Hindi audio and Hindi transcript and save them in the `audio` folder.
5. Enter the yt_audio_collector module using `cd yt_audio_collector` and change the protobuf version to 3.2 using `pip install protobuf==3.2`
6. Run `python system_2/preprocess_audio.py` then the system will preprocess the audio files for speech recognition and save them in the `preprocessed_audio` folder.

## Output

The output of the system is a set of preprocessed audio files that can be used as input for a speech recognition model. Each audio file is named as `<video_id>_<segment_number>.wav`, where `<video_id>` is the ID of the video from which the audio is extracted and `<segment_number>` is the number of the segment based on the transcript. The preprocessed audio files have the following properties:

- Frame rate: 16 kHz
- Sample width: 16 bits
- Number of channels: 1 (mono)
- Vocals extracted