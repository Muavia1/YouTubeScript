import gradio as gr
import whisper
import os
from transformers import pipeline

# Load models
model = whisper.load_model("base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def write_vtt(result, filename="output.vtt"):
    with open(filename, 'w') as srt_file:
        for idx, segment in enumerate(result['segments'], start=1):
            start = format_vtt_timestamp(segment['start'])
            end = format_vtt_timestamp(segment['end'])
            text = segment['text']
            srt_file.write(f"{idx}\n{start} --> {end}\n{text}\n\n")


def format_vtt_timestamp(seconds):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def inference(choice, link, mode, selected_language, audio_file):
    output_file = "audio.mp3"

    # Remove previous audio file if exists
    if os.path.exists(output_file):
        os.remove(output_file)

    if choice == "YouTube Video":
        if not link:
            return "Please provide a YouTube link.", None
        os.system(f"yt-dlp -x --audio-format mp3 -o '{output_file}' {link}")
    elif choice == "Audio File":
        if not audio_file:
            return "Please upload an audio file.", None
        audio_path = audio_file.name
        os.rename(audio_path, output_file)

    # Perform transcription
    if not mode or mode == "Original":
        result = model.transcribe(output_file, word_timestamps=True)
    else:
        result = model.transcribe(
            output_file, task="translate", language=selected_language.lower(), word_timestamps=True
        )

    # Summarize the transcript
    transcript_text = result['text']
    if len(transcript_text.split()) > 20:  # Ensure there's enough content for summarization
        summary = summarizer(transcript_text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    else:
        summary = transcript_text
    vtt_file = "sub.vtt"

    if os.path.exists(vtt_file):
        os.remove(vtt_file)

    write_vtt(result, vtt_file)

    return summary, 'sub.vtt'


# List of available languages in Whisper (excluding the original language)
available_languages = [lang.capitalize() for lang in whisper.tokenizer.LANGUAGES.keys() if lang != "english"]

title = "YouTubeScript"
description = "Get Any YouTube Video or Audio File Transcript!!!"
block = gr.Blocks()

with block:
    gr.Markdown(
        """# YouTubeScript
Get your YouTube transcription or upload audio files easily!
        """
    )

    # Choice selection: YouTube or Audio File
    with gr.Row():
        choice = gr.Radio(["YouTube Video", "Audio File"], label="Choose Input Type")

    # YouTube input
    youtube_link = gr.Textbox(label="YouTube Video Link", visible=False)
    choice.change(lambda x: gr.update(visible=(x == "YouTube Video")), inputs=choice, outputs=youtube_link)

    # Audio file input
    audio_file = gr.File(label="Upload Audio File", visible=False)
    audio_player = gr.Audio(label="Play Uploaded Audio", type="filepath", visible=False)

    def show_audio_player(file):
        if file:
            return gr.update(visible=True, value=file.name)
        return gr.update(visible=False)

    choice.change(lambda x: gr.update(visible=(x == "Audio File")), inputs=choice, outputs=[audio_file])
    audio_file.change(show_audio_player, inputs=audio_file, outputs=audio_player)

    # Mode selection and language dropdown
    with gr.Row():
        mode = gr.Radio(["Original", "Translate"], label="Mode", value=None)
    language_dropdown = gr.Dropdown(available_languages, label="Select Language for Translation", visible=False)

    def toggle_language_dropdown(mode):
        return gr.update(visible=(mode == "Translate"))

    mode.change(toggle_language_dropdown, inputs=[mode], outputs=[language_dropdown])

    btn = gr.Button("Get YouTubeScript 🪄")

    text = gr.Textbox(
        label="Transcript Summary",
        placeholder="Summary Output",
        lines=5
    )

    # Transcript file for download
    transcription = gr.File()

    # Clear button functionality
    def clear_fields():
        return gr.update(value=None),gr.update(value=None), gr.update(value=None), gr.update(value=None), gr.update(visible=False, value=None), gr.update(value=""), gr.update(value=None), gr.update(visible=False)

    clear_btn = gr.Button("Clear Fields 🧹")

    btn.click(inference, inputs=[choice, youtube_link, mode, language_dropdown, audio_file], outputs=[text, transcription])
    clear_btn.click(clear_fields, outputs=[choice,youtube_link, audio_file, mode, language_dropdown, text, transcription, audio_player])

block.launch(debug=True,share=True)
