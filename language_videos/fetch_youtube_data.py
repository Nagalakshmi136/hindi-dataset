import urllib.request
import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List

def get_video_ids(query:str)->List[str]:
    query = query.replace(' ','+')
    total_video_ids = []
    for i in range(5):
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}&sp=EgQoATAB")
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        total_video_ids.extend(video_ids)
    return list(set(total_video_ids))

def get_video_transcripts(query: str)->dict:
    video_ids = get_video_ids(query)
    transcript_results = {}
    for video in video_ids:
        try :
            transcript_list = YouTubeTranscriptApi.list_transcripts(video)
            transcript=transcript_list.find_manually_created_transcript(language_codes=['hi'])
            transcript_results[video]=transcript.fetch()
        except:
            continue
    return transcript_results

