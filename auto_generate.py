from youtube_transcript_api import YouTubeTranscriptApi

video_id = "RlPNh_PBZb4"
try:
    a = YouTubeTranscriptApi.get_transcript(video_id, languages="en")
    print(a)
except Exception as e:
    print(e)
