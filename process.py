from moviepy.editor import *
from moviepy.config import change_settings
# Load the video clip
import whisper
from os.path import join
from transformers import AutoModelWithLMHead,AutoTokenizer,pipeline
from pathlib import Path
from pydub import AudioSegment
import chinese_converter
from youtube_transcript_api import YouTubeTranscriptApi # two ways to retrieve the transcript

def ts(model_name):
    model = AutoModelWithLMHead.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)
    return translation

def get_caption_from_audioSegment(model_name, music_file):
    """
    Unsupported Chinese Language for now.
    Args:
        model_name (_type_): use pretrained model to translate the text
        music_file (_type_): _description_
    Returns:
        _type_: _description_
    """
    captions = []
    model = whisper.load_model("small")
    result = model.transcribe(music_file,no_speech_threshold=0.4)
    translation = ts(model_name)
    for idx, seg in enumerate(result['segments']):
        caption = {}
        start_ = float(result['segments'][idx]['start'])
        end_ = float(result['segments'][idx]['end'])
        caption["start"] = start_
        caption["end"] = end_
        txt = result['segments'][idx]['text']
        translated = translation(txt)
        caption["txt"] = txt + "\n" + translated[0]['translation_text']
        captions.append(caption)
    return captions

def get_caption_from_youtube_script(model_name, video_id):
    """
    Args:
        model_name (_type_): _description_
        video_id (_type_): _description_
    Returns:
        _type_: _description_
    """
    captions = []
    # get English transcript for a video.
    english = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    # get Chinese transcript for a video from youtube transcript
    # if there is no chinese transcript, 
    # we use the translation to generate the chinese transcript
    error = False
    try:
        chinese = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hans','zh-Hant'])
    except:
        translation = ts(model_name)
        error = True
    for idx, seg in enumerate(english):
        caption = {}
        start_ = float(english[idx]['start'])
        end_ = start_ + float(english[idx]['duration'])
        caption["start"] = start_
        caption["end"] = end_
        txt = english[idx]['text'].replace("\n", " ").replace("♪", "")
        if error:
            translated = translation(txt)[0]['translation_text']
        else:
            translated = chinese[idx]['text'].replace("\n", " ").replace("♪", "")
        caption["txt"] = txt + "\n" + translated
        print(caption)
        captions.append(caption)
    return captions

# Function to generate a TextClip. You can customize the appearance here
def generate_caption(clip, txt, start, end):
    w, h = clip.size
    custom_font_path = "/Users/aaron/work_dir/4KVideos/font/MaShanZheng-Regular.ttf"  # Replace with the path to your .ttf file
    txt_clip = TextClip(txt, fontsize=40, color='white', font=custom_font_path)
    txt_clip = txt_clip.set_pos(('center', h - txt_clip.size[1] - 10)).set_duration(end-start).set_start(start)
    return txt_clip

if __name__ == "__main__":
    AUDIO_FILE = r"origin_audios/y2mate.is - 胡夏 Xia Hu Those Bygone Years 那些年-KqjgLbKZ1h0-192k-1694863939.mp3" #ENDS WITH WAV or MP3 but MP3 needs to be converted to WAV
    VIDEO_FILE = r"origin_videos/yt5s.io-Olivia Rodrigo - get him back! (Official Video)-(1080p).mp4" #ENDS WITH MP4
    VIDEO_ID = "ZsJ-BHohXRI"
    MODEL_NAME = 'liam168/trans-opus-mt-en-zh'
    OUTPUT_MUSIC_PATH = "wav_audios/"
    MODE = 2
    assert (MODE != 2) or (VIDEO_ID != "") # if given Mode = 2, you should give the VIDEO_ID
    assert (MODE != 1) or AUDIO_FILE.endswith("wav") or AUDIO_FILE.endswith("mp3")
    assert VIDEO_FILE.endswith("mp4")
    print("Get the video captions...")
    assert MODE in [1,2,3] 
    # When mode == 1, then we use the audio file to generate the captions.
    # When mode == 2, then we use the youtube transcript to generate the captions
    # When mode == 3, then we use the lyric search to generate the captions 
    if MODE == 1:
        captions = get_caption_from_audioSegment(MODEL_NAME,AUDIO_FILE)
        if AUDIO_FILE.endswith("mp3"):
            sound = AudioSegment.from_file(AUDIO_FILE)
            print(f"exporting {AUDIO_FILE} to wav...")
            mp3_name = Path(AUDIO_FILE).stem
            sound.export(join(OUTPUT_MUSIC_PATH,f"{mp3_name}.wav"), format="wav")
            AUDIO_FILE = join(OUTPUT_MUSIC_PATH,f"{mp3_name}.wav")
    elif MODE == 2:
        captions = get_caption_from_youtube_script(MODEL_NAME,VIDEO_ID)
    elif MODE == 3:
        raise NotImplementedError
    # if not SAVE_N_CHECK:  
    video = VideoFileClip(VIDEO_FILE)
    # Create the caption clips
    caption_clips = [generate_caption(video, **caption) for caption in captions]

    # Overlay the captions on the video
    final = CompositeVideoClip([video] + caption_clips)
    print("Write the video to file...")
    # Export the video with captions
    final.write_videofile(
        VIDEO_FILE + "_caption.mp4",
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True)

   
