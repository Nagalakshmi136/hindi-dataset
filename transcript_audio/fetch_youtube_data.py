"""Fetching video Ids which have hindi audio and hindi transcripts 
from all videos of query get from youtube

"""
import json
import re
import urllib.request
from typing import Container, List

from youtube_transcript_api import YouTubeTranscriptApi

from constants import BASE_PATH, HINDI_RE_PATTERN
from transcript_audio.convert_to_audio import duration_of_video, has_hindi_audio
from utils.file_utils import create_dir

def get_video_ids(query: str) -> List[str]:
    """Fetching all videos corresponding to query from youtube

    Args:
        query (str): search query

    Returns:
        List[str]: List of video ids get from youtube based on given query
    """
    query = query.replace("_", "+")
    total_video_ids = []
    for i in range(5):
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={query}&sp=EgQoATAB"
        )
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        total_video_ids.extend(video_ids)
    return list(set(total_video_ids))


def is_valid_hindi_transcript(transcript: List[dict], video_id: str) -> bool:
    """Checking given transcript is valid
    i.e. given transcript is:
    1. In hindi.
    2. Exist for full video without empty text.
    Args:
        transcript (List[dict]): List of transcriptions of a video
        video_id (str): Id of the video

    Returns:
        bool: True for valid and vice versa
    """
    transcript_length = len(transcript)
    empty_text_count = 0
    hindi_to_total_text_ratio = 0
    subtitles_duration = 0
    for i in range(transcript_length):
        transcript_text = transcript[i].get("text")
        # Checking empty transcript text
        if re.sub("[\s+]", "", transcript_text) == "":
            empty_text_count += 1
            if empty_text_count > 10:
                return False
            continue
        hindi_chars = re.findall(HINDI_RE_PATTERN, transcript_text)
        len_hindi_chars = len(hindi_chars)
        len_total_chars = len(transcript_text)
        subtitles_duration += transcript[i].get("duration")
        # Checking the transcript is hindi or not
        if hindi_to_total_text_ratio == 0:
            hindi_to_total_text_ratio = round(len_hindi_chars / len_total_chars, 4)
        else:
            hindi_to_total_text_ratio = round(
                (hindi_to_total_text_ratio + len_hindi_chars / len_total_chars) / 2, 4
            )
    # Checking the transcripts exist for full video
    if subtitles_duration < 0.5 * duration_of_video(video_id):
        return False
    if hindi_to_total_text_ratio * 100 < 40:
        return False
    return True


def get_valid_video_ids(query: str, status_container: Container) -> List[str]:
    """Finding video ids which have hindi audio and hindi transcript from youtube

    Args:
        query (str): Represents the data you need
        status_container (Container): To store status of the program

    Returns:
        List[str]: list of valid video ids
    """
    create_dir(BASE_PATH/'temp')
    # Fetching all video ids
    video_ids = get_video_ids(query)
    print(f"{video_ids} all")
    transcript_results = {}
    for video in video_ids:
        try:
            # Fetching transcript
            transcript_status = status_container.status(
                f"finding transcription of {video}"
            )
            transcript_list = YouTubeTranscriptApi.list_transcripts(video)
            transcript = transcript_list.find_manually_created_transcript(
                language_codes=["hi"]
            )
            video_transcript = transcript.fetch()
            # Checking valid transcript or not
            if is_valid_hindi_transcript(video_transcript, video) == True:
                transcript_status.update(
                    label="found hindi transcription", state="complete"
                )
                print(f"{video} sub")
                audio_status = status_container.status(f"finding audio of {video}")
                # Checking valid audio or not
                if has_hindi_audio(video, query):
                    print(f"{video} aud")
                    audio_status.update(label="found hindi audio", state="complete")
                    transcript_results[video] = video_transcript

        except:
            continue
    # Storing the transcript in a json file
    if transcript_results:
        with open(f"{BASE_PATH}/audio/{query}/{query}.json", "w") as fp:
            json.dump(transcript_results, fp, indent=4, ensure_ascii=False)
    
    return transcript_results.keys()
