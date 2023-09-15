import urllib.request
import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
import constants as ct
from language_videos.convert_to_audio import has_hindi_audio
from language_videos.convert_to_audio import duration_of_video
import json


def get_video_ids(query: str) -> List[str]:
    query = query.replace(" ", "+")
    total_video_ids = []
    for i in range(5):
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={query}&sp=EgQoATAB"
        )
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        total_video_ids.extend(video_ids)
    return list(set(total_video_ids))


def is_valid_hindi_transcript(transcript: List[dict], videoId: str) -> bool:
    len_transcript = len(transcript)
    count_empty_text = 0
    ratio_hindi_total_text = 0
    duration_of_subtitles = 0
    for i in range(len_transcript):
        transcript_text = transcript[i].get("text")
        if re.sub("[\s+]", "", transcript_text) == "":
            count_empty_text += 1
            if count_empty_text > 10:
                return False
            continue
        hindi_chars = re.findall(ct.HINDI_RE_PATTERN, transcript_text)
        len_hindi_chars = len(hindi_chars)
        len_total_chars = len(transcript_text)
        duration_of_subtitles += transcript[i].get("duration")
        if ratio_hindi_total_text == 0:
            ratio_hindi_total_text = round(len_hindi_chars / len_total_chars, 4)
        else:
            ratio_hindi_total_text = round(
                (ratio_hindi_total_text + len_hindi_chars / len_total_chars) / 2, 4
            )
    if duration_of_subtitles < 0.5 * duration_of_video(videoId):
        return False
    if ratio_hindi_total_text * 100 < 40:
        return False
    return True


def get_valid_videos_id(query: str) -> dict:
    video_ids = get_video_ids(query)
    query = query.replace(" ", "_")
    transcript_results = {}
    for video in video_ids:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video)
            transcript = transcript_list.find_manually_created_transcript(
                language_codes=["hi"]
            )
            video_transcript = transcript.fetch()
            if is_valid_hindi_transcript(video_transcript, video) == True:
                if has_hindi_audio(video, query):
                    transcript_results[video] = video_transcript

        except:
            continue
    if transcript_results:
        with open(f"{ct.BASE_PATH}/transcripts/{query}.json", "w") as fp:
            json.dump(transcript_results, fp, indent=4, ensure_ascii=False)
    return transcript_results.keys()
