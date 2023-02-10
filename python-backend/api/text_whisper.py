from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import torch
import os
import gradio as gr
import whisper
from whisper import tokenizer
import time

current_size = 'tiny'
AUTO_DETECT_LANG = "Auto Detect"

# load model and processor
# processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
# model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")

model = whisper.load_model(current_size)


def transcribe(audio, state={}, model_size='tiny', delay=1.2, lang=None, translate=False):
    time.sleep(delay - 1)

    global current_size
    global model
    if model_size != current_size:
        current_size = model_size
        model = whisper.load_model(current_size)

    transcription = model.transcribe(
        audio,
        language=lang if lang != AUTO_DETECT_LANG else None
    )
    state['transcription'] += transcription['text'] + " "

    if translate:
        x = whisper.load_audio(audio)
        x = whisper.pad_or_trim(x)
        mel = whisper.log_mel_spectrogram(x).to(model.device)

        options = whisper.DecodingOptions(task="translation")
        translation = whisper.decode(model, mel, options)

        state['translation'] += translation.text + " "

    return state['transcription'], state['translation'], state, f"detected language: {transcription['language']}"


title = "OpenAI's Whisper Real-time Demo"
description = "A simple demo of OpenAI's [**Whisper**](https://github.com/openai/whisper) speech recognition model. This demo runs on a CPU. For faster inference choose 'tiny' model size and set the language explicitly."

model_size = gr.Dropdown(label="Model size", choices=[
                         'base', 'tiny', 'small', 'medium', 'large'], value='base')

delay_slider = gr.inputs.Slider(
    minimum=1, maximum=5, default=1.2, label="Rate of transcription")

available_languages = sorted(tokenizer.TO_LANGUAGE_CODE.keys())
available_languages = [lang.capitalize() for lang in available_languages]
available_languages = [AUTO_DETECT_LANG]+available_languages

lang_dropdown = gr.inputs.Dropdown(
    choices=available_languages, label="Language", default=AUTO_DETECT_LANG, type="value")

if lang_dropdown == AUTO_DETECT_LANG:
    lang_dropdown = None

translate_checkbox = gr.inputs.Checkbox(
    label="Translate to English", default=False)


transcription_tb = gr.Textbox(label="Transcription", lines=10, max_lines=20)
translation_tb = gr.Textbox(label="Translation", lines=10, max_lines=20)
detected_lang = gr.outputs.HTML(label="Detected Language")

state = gr.State({"transcription": "", "translation": ""})

gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(source="microphone", type="filepath", streaming=True),
        state,
        model_size,
        delay_slider,
        lang_dropdown,
        translate_checkbox
    ],
    outputs=[
        transcription_tb,
        translation_tb,
        state,
        detected_lang
    ],
    live=True,
    allow_flagging='never',
    title=title,
    description=description,
).launch(
    # enable_queue=True,
    # debug=True
)
