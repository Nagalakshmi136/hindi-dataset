"""
Splitting audio based on transcript
"""
import sys

import csv
import json

import os
from pathlib import Path

from pydub import AudioSegment

sys.path.append("..")
from yt_audio_collector.utils.file_utils import create_dir, load_json, resolve_path


BASE_PATH = Path(os.getcwd()).parent


class PreProcessAudio:
    """
    This class is responsible for preprocessing the audio for speech recognition model.
    It extracts vocals from audio files,
    resamples the audio, and divides the audio into chunks based on transcriptions.
    """

    def __init__(
        self, source_path: str, destination_path: str, background_sound: bool = False
    ) -> None:
        """
        Initializes the PreProcessAudio class.

        Attributes:
        -----------
        source_path: `Path`
            The path of the source audio files.
        destination_path: `Path`
            The path where the processed audio files will be stored.
        background_sound: `bool`
            A boolean value indicating whether to extract vocals from the audio files or not.
        """
        self.sample_rate = 16000
        self.width_rate = 2
        self.channels = 1
        self.background_sound = background_sound
        self.destination_path = Path(destination_path)
        self.temp = create_dir(BASE_PATH / "temp")
        self.source_path = Path(source_path)

    def get_file_name(self, total_file_path: Path) -> str:
        """Finds the file name without extension from absolute file path

        Parameters:
        -----------
        total_file_path: `Path`
            The absolute path of the file

        Return:
        -------
        str
            File name without extension
        """
        base_name = os.path.basename(total_file_path)
        return os.path.splitext(base_name)[0]

    def extract_vocals(self, chunk_path: str) -> None:
        """
        Extracts vocals from audio file using spleeter library and store it in the temporary file(temp).

        Parameters:
        -----------
        chunk_path: `str`
            The path of the audio file.
        """
        os.system(
            f"spleeter separate -p spleeter:2stems -o {self.temp} {chunk_path}.wav"
        )

    def resample(self, chunk_path: str, destination_chunk_path: str) -> None:
        """
        Changes the sample rate, sample width, channels of the the given audio file .

        Parameters:
        -----------
        chunk_path: `str`
            The audio file path before resampling.
        destination_chunk_path: `str`
            The audio fille path after resampling.
        """
        vocals_audio = AudioSegment.from_file(f"{chunk_path}.wav")
        # set sample frame rate
        vocals_audio = vocals_audio.set_frame_rate(self.sample_rate)
        # set sample width
        vocals_audio = vocals_audio.set_sample_width(self.width_rate)
        # set channels
        vocals_audio = vocals_audio.set_channels(self.channels)
        vocals_audio.export(f"{destination_chunk_path}.wav", format="wav")

    def preprocess_audio_chunks(self, category_path: str) -> None:
        """
        Divides the audio into chunks based on the transcriptions and preprocess the audio chunks.

        Parameters:
        -----------
        category_path: `str`
            The category name in the audio folder.
        """
        # Make a JSON file which contains all the processed audio ids
        # which helps to track the processed audio files in one place and
        # avoid processing of the same audio repeatedly.
        processed_audio_file_path = self.destination_path / "processed_audios.json"

        if not processed_audio_file_path.exists():
            processed_audio_file_path.touch()

        processed_audios = load_json(processed_audio_file_path)

        if not processed_audios.get(category_path):
            processed_audios[category_path] = []

        audio_files_path = resolve_path(self.source_path / category_path)
        subtitles_data = load_json(audio_files_path / f"{category_path}.json")
        destination_category_path = create_dir(self.destination_path / category_path)

        for audio_file_path in audio_files_path.glob("*.mp3"):
            audio_id = self.get_file_name(audio_file_path)

            if audio_id not in processed_audios[category_path]:
                audio = AudioSegment.from_file_using_temporary_files(audio_file_path)
                destination_audio_path = create_dir(
                    destination_category_path / audio_id
                )
                subtitles = subtitles_data[audio_id]

                with open(
                    f"{destination_audio_path}/subtitles.txt", "w"
                ) as file_writer:
                    csv_writer = csv.writer(file_writer)

                    for subtitle in subtitles:
                        start_time = subtitle.get("start") * 1000
                        end_time = start_time + subtitle.get("duration") * 1000
                        chunk = audio[start_time:end_time]
                        chunk_name = f"{audio_id}_{start_time}_{end_time}"
                        chunk_path = f"{self.temp}/{chunk_name}"
                        chunk.export(f"{chunk_path}.wav", format="wav")

                        # extract vocals from the chunk of audio file
                        if not self.background_sound:
                            self.extract_vocals(chunk_path)
                            chunk_path = f"{chunk_path}/vocals"

                        # resampling the extracted audio chunk
                        self.resample(
                            chunk_path, f"{destination_audio_path}/{chunk_name}"
                        )

                        # remove temporarily stored data
                        os.system(f"rm -rf {self.temp}/*")

                        # write into the csv transcription file
                        csv_writer.writerow([chunk_name, subtitle.get("text")])

                processed_audios[category_path].append(audio_id)
        # update the processed_audios.json file
        with open(processed_audio_file_path, "w", encoding="utf-8") as file_writer:
            json.dump(processed_audios, file_writer, indent=4)

    def preprocess_audio(self):
        """
        Traverses through all categories of audio and preprocess the audio.
        """
        create_dir(self.destination_path)
        for category_path in self.source_path.glob("*"):
            category_name = category_path.name
            self.preprocess_audio_chunks(category_name)


PreProcessAudio(
    f"{BASE_PATH}/audio", f"{BASE_PATH}/processed_audio", False
).preprocess_audio()
