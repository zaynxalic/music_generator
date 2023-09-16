# import whisper
# import ffmpeg

# model = whisper.load_model("small")
# music_file = "/Users/aaron/work_dir/4KVideos/wav_audios/vampire.wav"
# result = model.transcribe(music_file,no_speech_threshold=0.4)
# for idx, seg in enumerate(result['segments']):
#     result['segments'][idx]['text']
#     result['segments'][idx]['start']
    
# # duration = float(ffmpeg.probe(music_file)['format']['duration'])
# # load audio and pad/trim it to fit 30 seconds
# # audio = whisper.load_audio(music_file)
# # audio = whisper.pad_or_trim(audio)
# # # make log-Mel spectrogram and move to the same device as the model
# # mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # # detect the spoken language
# # _, probs = model.detect_language(mel)
# # print(f"Detected language: {max(probs, key=probs.get)}")

# # # decode the audio
# options = whisper.DecodingOptions(fp16 = False, task=translate)
# result = whisper.decode(model, mel, options)

# # print the recognized text
# print(result)

from transformers import AutoModelWithLMHead,AutoTokenizer,pipeline,AutoModelForSeq2SeqLM
# mode_name = 'liam168/trans-opus-mt-en-zh'
# model = AutoModelWithLMHead.from_pretrained(mode_name)
# tokenizer = AutoTokenizer.from_pretrained(mode_name)
# translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)
# t = translation('Be aware that you SHOULD NOT rely on t5-base automatically truncating your input to 512 when padding/encoding.', max_length=400)

