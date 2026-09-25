import os
import gradio as gr
from deep_translator import GoogleTranslator

# ---------------- LANGUAGE LIST ----------------

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


# ---------------- TRANSLATION FUNCTION ----------------

def translate_text(text, source, target):

    if not text or not text.strip():
        return "Please enter some text."

    if source == target:
        return text

    try:
        translator = GoogleTranslator(
            source=languages[source],
            target=languages[target]
        )

        translated_text = translator.translate(text)

        if translated_text:
            return translated_text

        return "Translation failed. Please try again."

    except Exception as e:
        return f"Translation error: {str(e)}"


# ---------------- GRADIO APP ----------------

with gr.Blocks(
    title="AI Language Translator",
    theme=gr.themes.Soft()
) as app:

    gr.Markdown(
        "# 🌍 AI Language Translation Tool"
    )

    gr.Markdown(
        "Translate text instantly between multiple languages"
    )

    # Text input
    text_input = gr.Textbox(
        label="Enter text",
        placeholder="Type your text here..."
    )

    # Language selection
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

    # Translate button
    translate_button = gr.Button(
        "Translate",
        variant="primary"
    )

    # Output
    output = gr.Textbox(
        label="Translated Text",
        interactive=False
    )

    # Button action
    translate_button.click(
        fn=translate_text,
        inputs=[text_input, source, target],
        outputs=output
    )


# ---------------- LAUNCH APP ----------------

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)