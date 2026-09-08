import os
import gradio as gr
from deep_translator import MyMemoryTranslator

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar"
}

def translate_text(text, source, target):
    if not text.strip():
        return "Please enter some text."

    if source == target:
        return text

    try:
        translator = MyMemoryTranslator(
            source=languages[source],
            target=languages[target]
        )
        return translator.translate(text)
    except Exception as e:
        return f"Translation error: {e}"

with gr.Blocks(title="AI Language Translator") as app:
    gr.Markdown("# 🌍 AI Language Translation Tool")
    gr.Markdown("Translate text instantly between multiple languages")

    text_input = gr.Textbox(
        label="Enter text",
        placeholder="Type your text here..."
    )

    with gr.Row():
        source = gr.Dropdown(
            choices=list(languages.keys()),
            value="English",
            label="Source Language"
        )

        target = gr.Dropdown(
            choices=list(languages.keys()),
            value="Hindi",
            label="Target Language"
        )

    translate_button = gr.Button("Translate")
    output = gr.Textbox(label="Translated Text")

    translate_button.click(
        translate_text,
        inputs=[text_input, source, target],
        outputs=output
    )

translate_button = translate_button

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)