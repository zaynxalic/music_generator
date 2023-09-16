import numpy as np
import os 
from moviepy.editor import *
import re
from moviepy.config import change_settings
# change_settings({"IMAGEMAGICK_BINARY": "/usr/local/Cellar/imagemagick/6.9.6-2/bin/convert"})
# Load the video clip
video = VideoFileClip("/Users/aaron/work_dir/4KVideos/origin_videos/y2mate.is - Ne Yo So Sick Official Music Video -IxszlJppRQI-1080pp-1693650425.mp4")

def extract(text, pattern):
    matches_x = re.findall(pattern, text)
    if not matches_x:
        return None
    match = matches_x[0]
    minutes = int(match[0])
    seconds = float(match[1])
    total_seconds = minutes * 60 + seconds
    text = match[2]
    return total_seconds, text


def read(lrc, chineselrc):
    pattern = r'\[(\d+):(\d+\.\d+)\](.+)'
    caption = []
    with open(lrc) as f1, open(chineselrc) as f2: 
        for x, y in zip(f1, f2):
            if extract(x, pattern) and extract(y, pattern):
                start, text1 = extract(x, pattern)
                _, text2 = extract(y, pattern)
                text = text1 + '\n' + text2
                caption.append({
                    "txt": text,
                    "start": start - 1.5,
                    "end": start - 1.5 + 1
                })
    return caption
            

# Manually define the captions and their start and end times with millisecond precision
# captions = [
    # {
    #     "txt": "This is the first caption.",
    #     "start": 1.250,  # Starts at 1.250 seconds (or 1250 milliseconds)
    #     "end": 4.785     # Ends at 4.785 seconds (or 4785 milliseconds)
    # },
    # {
    #     "txt": "This is the second caption.",
    #     "start": 5.100,
    #     "end": 8.610
    # }
    # Add more captions as needed
# ]
captions = read("/Users/aaron/work_dir/4KVideos/lyrics/So Sick by Ne Yo.lrc", "/Users/aaron/work_dir/4KVideos/lyrics/So Sick by Ne yo Chinese.lrc")
# Function to generate a TextClip. You can customize the appearance here
def generate_caption(clip, txt, start, end):
    custom_font_path = "/Users/aaron/work_dir/4KVideos/font/MaShanZheng-Regular.ttf"  # Replace with the path to your .ttf file
    txt_clip = TextClip(txt, fontsize=36, color='black', font=custom_font_path)
    txt_clip = txt_clip.set_pos('bottom').margin(bottom=10, opacity=0).set_duration(end-start).set_start(start)
    return txt_clip

# Create the caption clips
caption_clips = [generate_caption(video, **caption) for caption in captions]

# Overlay the captions on the video
final = CompositeVideoClip([video] + caption_clips)

# Export the video with captions
final.write_videofile(
    "/Users/aaron/work_dir/4KVideos/upscaled_audios/output_video_with_manual_subs_precise.mp4",
    audio_codec='aac', 
    temp_audiofile='temp-audio.m4a', 
    remove_temp=True)

   
