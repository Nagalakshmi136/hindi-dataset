import sys

sys.path.append("..")

import csv
import json

import os
from pathlib import Path

from pydub import AudioSegment

from utils.file_utils import create_dir, load_json, resolve_path



BASE_PATH = Path(os.getcwd()).parent


class PreProcessAudio:
    def __init__(
        self, source_path: Path, destination_path: Path, background_sound: bool
    ) -> None:
        
        self.sample_rate = 16000
        self.width_rate = 2
        self.channels = 1
        self.base_path = BASE_PATH
        self.background_sound = background_sound
        self.destination_path = destination_path
        self.temp = create_dir(BASE_PATH / "temp")
        self.source_path = source_path

    def get_file_name(self, total_file_path: Path) -> str:
        """
        Fetching the name of the file from total path of the file

        Parameters:
        -----------
        total_file_path: `Path`
            Full path of the file

        Returns:
        --------
        `str`
            Name of the file without extension
        """
        base_name = os.path.basename(total_file_path)
        return os.path.splitext(base_name)[0]

    def extract_vocals(self, chunk_path: str) -> None:
        """Extracting vocals from audio file

        Args:
            chunk_path (str): the path of the audio file
        """
        os.system(
            f"spleeter separate -p spleeter:2stems -o {self.temp} {chunk_path}.wav"
        )

    def resample(self, chunk_path: str, destination_chunk_path: str) -> None:
        """Change the sample rate, sample width, channels of the the given audio

        Args:
            chunk_path (str): The audio file path before changing
            destination_chunk_path (str): The audio fille path after changing
        """
        vocals_audio = AudioSegment.from_file(f"{chunk_path}.wav")
        # set sample frame rate
        vocals_audio = vocals_audio.set_frame_rate(self.sample_rate)
        # set sample width
        vocals_audio = vocals_audio.set_sample_width(self.width_rate)
        # set channels
        vocals_audio = vocals_audio.set_channels(self.channels)
        vocals_audio.export(f"{destination_chunk_path}.wav", format="wav")

    def get_audio_chunks(self, category_path: str) -> None:
        """Diving the audio into chunks based on the transcriptions

        Args:
            category_path (str): the category name in the audio folder
        """
        processed_audio_file_path = self.destination_path / "processed_audios.json"
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
                destination_audio_path = create_dir(destination_category_path / audio_id)
                subtitles = subtitles_data[audio_id]
                subtitle_csv_file = open(
                    f"{destination_audio_path}/subtitles.csv", "w", newline=""
                )
                csv_writer = csv.writer(subtitle_csv_file)

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
                    self.resample(chunk_path, f"{destination_audio_path}/{chunk_name}")
                    # remove temporarily stored data
                    os.system(f"rm -rf {self.temp}/*")
                    # write into the csv transcription file
                    csv_writer.writerow([chunk_name, subtitle.get("text")])
                    break

                subtitle_csv_file.close()
                processed_audios[category_path].append(audio_id)
        # update processed the data file
        with open(processed_audio_file_path, "w") as file_writer:
            json.dump(processed_audios, file_writer, indent=4)

    def get_processed_audio(self):
        create_dir(self.destination_path)
        processed_audio_file = open(
            self.destination_path / "processed_audios.json", "w"
        )
        processed_audio_file.close()
        for category_path in self.source_path.glob("*"):
            category_name = category_path.name
            self.get_audio_chunks(category_name)


PreProcessAudio(
    BASE_PATH / "audio", BASE_PATH / "search_data", False
).get_processed_audio()
