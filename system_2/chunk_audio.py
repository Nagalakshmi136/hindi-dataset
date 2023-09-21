from pydub import AudioSegment
from utils.file_utils import resolve_path
from utils.file_utils import load_json
from utils.file_utils import create_dir
from constants import BASE_PATH
import os
import csv
import json


def get_audio_chunks(query: str):
    JSON_PATH = BASE_PATH/'search_data'/'processed_videos.json'
    processed_videos = load_json(JSON_PATH) 
    if not processed_videos.get(query):
        processed_videos[query] = []
    audio_files_path = resolve_path(BASE_PATH / "audio" / query)
    subtitles_data = load_json(BASE_PATH / "transcripts" / f"{query}.json")
    category_path = create_dir(BASE_PATH / "search_data" / query)
    for audio_file_path in audio_files_path.glob("*"):
        audio_file_name = os.path.basename(audio_file_path)
        video_id = os.path.splitext(audio_file_name)[0]
        if video_id not in processed_videos[query]:
            audio = AudioSegment.from_file(audio_file_path)
            video_path = create_dir(category_path / video_id)
            subtitles = subtitles_data[video_id]
            subtitle_csv_file = open(f'{video_path}/subtitles.csv','w',newline='')
            csv_writer = csv.writer(subtitle_csv_file)
            for subtitle in subtitles:
                start_time = subtitle.get("start") * 1000
                end_time = start_time + subtitle.get("duration") * 1000
                chunk = audio[start_time:end_time]
                chunk_name = f"{video_id}_{start_time}_{end_time}"
                chunk.export(
                    f"{video_path}/{chunk_name}.wav", format="wav" 
                )
                csv_writer.writerow([chunk_name,subtitle.get('text')])
            subtitle_csv_file.close()
            processed_videos[query].append(video_id)
    with open(JSON_PATH,'w') as file_writer:
        json.dump(processed_videos,file_writer,indent=4)
    
        
