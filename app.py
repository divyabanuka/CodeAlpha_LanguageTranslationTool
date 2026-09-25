import os
import requests
import gradio as gr

# ---------------- LANGUAGE LIST ----------------

languages = {
    "English": "English",
    "Hindi": "Hindi",
    "Telugu": "Telugu",
    "Tamil": "Tamil",
    "Kannada": "Kannada",
    "Malayalam": "Malayalam",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Japanese": "Japanese",
    "Chinese": "Chinese",
    "Arabic": "Arabic"
}


# ---------------- GEMINI TRANSLATION ----------------

def translate_text(text, source, target):

    if not text or not text.strip():
        return "Please enter some text."

    if source == target:
        return text

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "Error: GEMINI_API_KEY is not configured."

    prompt = f"""
Translate the following text from {source} to {target}.

Return ONLY the translated text.
Do not add explanations, quotation marks, or extra text.

Text:
{text}
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-2.5-flash:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code != 200:
            return f"Translation error: {response.text}"

        result = response.json()

        translated_text = (
            result["candidates"][0]["content"]["parts"][0]["text"]
        )

        return translated_text.strip()

    except requests.exceptions.Timeout:
        return "Translation error: Request timed out. Please try again."

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

    translate_button = gr.Button(
        "Translate",
        variant="primary"
    )

    output = gr.Textbox(
        label="Translated Text",
        interactive=False
    )

    translate_button.click(
        fn=translate_text,
        inputs=[text_input, source, target],
        outputs=output
    )


# ---------------- START SERVER ----------------

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)