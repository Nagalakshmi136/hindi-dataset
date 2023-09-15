from pytube import YouTube
import os
from constants import BASE_PATH, BASE_URL
import whisper
from pathlib import Path

# import shutil


def get_audio_language(audio: str):
    model = whisper.load_model("base")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    return max(probs, key=probs.get)


def duration_of_video(videoId: str):
    url = f"{BASE_URL}{videoId}"
    yt = YouTube(url)
    return yt.length


def store_audio(query: str, audio_path: Path):
    destination_path = BASE_PATH / "audio" / query.replace(" ", "_") / audio_path.name
    if not destination_path.parent.exists():
        destination_path.parent.mkdir(parents=True)
    os.system(f"mv {str(audio_path)} {str(destination_path)}")


def video_to_audio(videoId: str) -> Path:
    url = f"{BASE_URL}{videoId}"
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    destination = BASE_PATH / "temp"
    out_file = video.download(output_path=destination)
    new_file = destination / f"{videoId}.mp3"
    os.rename(out_file, new_file)
    return destination / new_file


def has_hindi_audio(videoId: str, query: str):
    audio_file = video_to_audio(videoId)
    audio_language = get_audio_language(audio_file)
    if audio_language.lower() in ["hi"]:
        store_audio(query, audio_file)
        return True
    # Removing the audio file which is not hindi from temporary storage
    if os.path.exists(audio_file):
        os.remove(audio_file)
    return False
