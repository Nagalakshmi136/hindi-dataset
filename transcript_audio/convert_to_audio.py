import os
from pathlib import Path

import whisper
from pytube import YouTube

from constants import BASE_PATH, BASE_URL


def get_audio_language(audio: str) -> str:
    """Finding the language of an audio using whisper model

    Args:
        audio (str): The audio file path

    Returns:
        str: Language of the given audio
    """
    model = whisper.load_model("base")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    return detected_language


def duration_of_video(video_id: str) -> int:
    """Calculating the duration of given video

    Args:
        video_id (str): The id of the video

    Returns:
        int: Duration or length of the given video
    """
    url = f"{BASE_URL}{video_id}"
    yt = YouTube(url)
    return yt.length


def store_audio(query: str, audio_path: Path) -> None:
    """Storing the audio file in a separate audio folder

    Args:
        query (str): Represents the data you need
        audio_path (Path): The audio file path
    """
    destination_path = BASE_PATH / "audio" / query.replace(" ", "_") / audio_path.name
    if not destination_path.parent.exists():
        destination_path.parent.mkdir(parents=True)
    os.system(f"mv {str(audio_path)} {str(destination_path)}")


def video_to_audio(video_id: str) -> Path:
    """ Converting video to audio 

    Args:
        video_id (str): The id of the video

    Returns:
        Path: The converted audio file path
    """
    url = f"{BASE_URL}{video_id}"
    yt = YouTube(url)
    try:
        # Fetching the audio of the video with given id
        video = yt.streams.filter(only_audio=True).first()
    except Exception as e:
        print(e)
    destination = BASE_PATH / "temp"
    # Downloading the audio in temporary file and it gives audio file
    # but with mp4(video supported format) extension which we need to convert to mp3(audio supported format)
    output_file = video.download(output_path=destination)
    # Renaming the downloaded file with mp3
    new_file = destination / f"{video_id}.mp3"
    os.rename(output_file, new_file)
    return destination / new_file


def has_hindi_audio(video_id: str, query: str) -> bool:
    """Converts the video to audio and determine its audio language, 
    if it's hindi then store the audio and return true else removed and return false

    Args:
        video_id (str): The id of the video
        query (str): represents the data you need

    Returns:
        bool: True if audio language is hindi and vice versa
    """
    audio_file = video_to_audio(video_id)
    audio_language = get_audio_language(audio_file)
    print(audio_language)
    
    if audio_language.lower() in ["hi"]:
        store_audio(query, audio_file)
        return True
    # Removing the audio file which is not hindi from temporary storage
    if os.path.exists(audio_file):
        os.remove(audio_file)  # I wrote a method check utils files
    return False
