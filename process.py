import numpy as np
import os
from moviepy.editor import *
import re
from moviepy.config import change_settings
# Load the video clip
import whisper
import ffmpeg
from transformers import AutoModelWithLMHead,AutoTokenizer,pipeline
from pathlib import Path
MODEL_NAME = 'liam168/trans-opus-mt-en-zh'
def pipeline(model_name):
    model = AutoModelWithLMHead.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)
    return translation

def get_caption(music_file):
    captions = []
    model = whisper.load_model("small")
    result = model.transcribe(music_file,no_speech_threshold=0.4)
    translation = pipeline(MODEL_NAME)
    for idx, seg in enumerate(result['segments']):
        caption = {}
        start_ = float(result['segments'][idx]['start'])
        end_ = float(result['segments'][idx]['end'])
        caption["start"] = start_ if idx != 0 else max(end_ - 3.0, 0)
        caption["end"] = end_
        txt = result['segments'][idx]['text']
        translated = translation(txt)
        caption["txt"] = txt + "\n" + translated[0]['translation_text']
        print(caption)
        captions.append(caption)
    return captions

# Function to generate a TextClip. You can customize the appearance here
def generate_caption(clip, txt, start, end):
    custom_font_path = "/Users/aaron/work_dir/4KVideos/font/MaShanZheng-Regular.ttf"  # Replace with the path to your .ttf file
    txt_clip = TextClip(txt, fontsize=36, color='black', font=custom_font_path)
    txt_clip = txt_clip.set_pos('bottom').margin(bottom=10, opacity=0).set_duration(end-start).set_start(start)
    return txt_clip

if __name__ == "__main__":
    AUDIO_FILE = r"wav_audios/vampire.wav" #ENDS WITH WAV
    VIDEO_FILE = r"origin_videos/y2mate.is - Olivia Rodrigo vampire Official Video -RlPNh_PBZb4-1080pp-1693650167.mp4" #ENDS WITH MP4
    assert AUDIO_FILE.endswith("wav")
    assert VIDEO_FILE.endswith("mp4")
    print("Get the video captions...")
    captions = get_caption(AUDIO_FILE)
    video = VideoFileClip(VIDEO_FILE)
    # Create the caption clips
    caption_clips = [generate_caption(video, **caption) for caption in captions]

    # Overlay the captions on the video
    final = CompositeVideoClip([video] + caption_clips)
    print("Write the video to file...")
    # Export the video with captions
    final.write_videofile(
        Path(VIDEO_FILE).stem + "_caption.mp4",
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True)

   
