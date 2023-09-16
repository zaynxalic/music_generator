import numpy as np
import os
from pydub import AudioSegment
import subprocess
from os.path import join
from path import Path
ORIGIN_MUSIC_PATH = "origin_audios/"
OUTPUT_MUSIC_PATH = "wav_audios/"
def get_files(file):
    return [i for i in os.listdir(file) if ".mp3" in i]

if __name__ == "__main__":
    for mp3_file in get_files(ORIGIN_MUSIC_PATH):
        sound = AudioSegment.from_file(join(ORIGIN_MUSIC_PATH,mp3_file))
        print(f"exporting {mp3_file} to wav...")
        mp3_name = Path(mp3_file).stem
        sound.export(join(OUTPUT_MUSIC_PATH,f"{mp3_name}.wav"), format="wav")
