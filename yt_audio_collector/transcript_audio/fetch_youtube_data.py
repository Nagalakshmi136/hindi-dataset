import json
import re
import urllib.request
from typing import Container, List

from youtube_transcript_api import YouTubeTranscriptApi

from constants import BASE_PATH, HINDI_RE_PATTERN
from yt_audio_collector.transcript_audio.convert_to_audio import duration_of_video, has_hindi_audio
from yt_audio_collector.utils.file_utils import create_dir


def get_video_ids(query: str) -> List[str]:
    """
    Fetches all video ids corresponding to the given query from YouTube.

    Parameters:
    -----------
    query: `str`
        The search query.

    Return:
    -------
    List[str]
        A list of video ids fetched from YouTube based on the given query.
    """
    # Replace underscores with plus signs to match YouTube's search query format
    query = query.replace("_", "+")
    total_video_ids = []
    # While requesting the youtube server every time it gives slightly 
    # different results for the same query, to capture the majority no.of 
    # results request the server multiple times(say 5 here) and
    # and store all the results. 
    for i in range(5):        
        # Requests the youtube server using urllib library which gives html file
        # with the following url where sp=EgQoATAB helps to filter the 
        # results for the query with the features Subtitles/CC and Creative Commons
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={query}&sp=EgQoATAB"
        )
        # html contains the list of youtube video links, by using regex library
        # find all the video ids by matching the video id pattern in total html file
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        total_video_ids.extend(video_ids)
    # Remove duplicates and return unique results(video ids).
    return list(set(total_video_ids))


def is_valid_hindi_transcript(transcript: List[dict], video_id: str) -> bool:
    """
    Checks if the given transcript is valid:
    1. The transcript must be in Hindi.
    2. Exists for the full video without empty text.

    Parameters:
    -----------
    transcript: `List[dict]`
        A list of transcriptions of a video.
    video_id: `str`
        The ID of the video.

    Return:
    -------
    bool
        True if the transcript is valid, False otherwise.
    """
    transcript_length = len(transcript)
    empty_text_count = 0
    hindi_to_total_text_ratio = 0
    subtitles_duration = 0
    for i in range(transcript_length):
        transcript_text = transcript[i].get("text")
        # Check for empty transcript text
        if re.sub("[\s+]", "", transcript_text) == "":
            empty_text_count += 1
            # If there are more than 10 empty texts, the transcript is invalid
            if empty_text_count > 10:
                return False
            continue
        # Find all hindi characters in single transcript text
        hindi_chars = re.findall(HINDI_RE_PATTERN, transcript_text)
        len_hindi_chars = len(hindi_chars)
        len_total_chars = len(transcript_text)
        subtitles_duration += transcript[i].get("duration")
        # Calculate the ratio of Hindi characters to total characters 
        # of transcript
        if hindi_to_total_text_ratio == 0:
            hindi_to_total_text_ratio = round(len_hindi_chars / len_total_chars, 4)
        else:
            hindi_to_total_text_ratio = round(
                (hindi_to_total_text_ratio + len_hindi_chars / len_total_chars) / 2, 4
            )
    # Check if subtitles duration is < 50% of total duration of video then transcript is invalid
    if subtitles_duration < 0.5 * duration_of_video(video_id):
        return False
    # Check if the ratio of Hindi characters to total characters < 40% then transcript is invalid
    if hindi_to_total_text_ratio * 100 < 40:
        return False
    # If all checks pass, the transcript is valid
    return True


def get_valid_video_ids(query: str, status_container: Container) -> List[str]:
    """
    Finds video ids which have Hindi audio and Hindi transcript from YouTube.

    Parameters:
    -----------
    query: `str`
        The search query.
    status_container: `Container`
        A container to store the status of the program.

    Return:
    -------
    List[str]
        A list of valid video ids.
    """
    # To store files temporarily, here mainly for storing for audio files
    create_dir(BASE_PATH / "temp")
    # Fetch all video ids for the given query
    video_ids = get_video_ids(query)
    transcript_results = {}
    for video in video_ids:
        try:
            # Fetch the hindi transcript for the video id using youtube_transcript_api library 
            transcript_status = status_container.status(
                f"finding transcription of {video}"
            )
            transcript_list = YouTubeTranscriptApi.list_transcripts(video)
            transcript = transcript_list.find_manually_created_transcript(
                language_codes=["hi"]
            )
            video_transcript = transcript.fetch()
            # Check if the transcript is valid
            if is_valid_hindi_transcript(video_transcript, video) == True:
                transcript_status.update(
                    label="found Hindi transcription", state="complete"
                )
                # Check if the video has Hindi audio
                audio_status = status_container.status(f"finding audio of {video}")
                if has_hindi_audio(video, query):
                    audio_status.update(label="found Hindi audio", state="complete")
                    transcript_results[video] = video_transcript

        except:
            continue
    # Store the transcripts in a JSON file inside the folder which have audio files
    # for all the transcripts with the query name in audio folder
    if transcript_results:
        with open(
            f"{BASE_PATH}/audio/{query}/{query}.json", "w", encoding="utf-8"
        ) as json_file:
            json.dump(transcript_results, json_file, indent=4, ensure_ascii=False)

    # Return the list of valid video ids
    return transcript_results.keys()
