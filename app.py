import os
import time
import random
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


# ---------------- TRANSLATION FUNCTION ----------------

def translate_text(text, source, target):

    # Check empty input
    if not text or not text.strip():
        return "Please enter some text."

    # Same language
    if source == target:
        return text

    # Get API key from Render environment
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "Error: GEMINI_API_KEY is not configured."

    # Translation prompt
    prompt = f"""
Translate the following text from {source} to {target}.

Important instructions:
- Return ONLY the translated text.
- Do not add explanations.
- Do not add quotation marks.
- Do not add labels.
- Preserve the original meaning.

Text:
{text}
"""

    # Gemini API URL
    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.8-flash:generateContent"
    )

    # Headers
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    # Request data
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 500
        }
    }

    # ---------------- RETRY SYSTEM ----------------

    max_retries = 4

    for attempt in range(max_retries):

        try:

            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )

            # Successful response
            if response.status_code == 200:

                result = response.json()

                try:
                    translated_text = (
                        result["candidates"][0]
                        ["content"]["parts"][0]
                        ["text"]
                    )

                    return translated_text.strip()

                except (KeyError, IndexError, TypeError):

                    return "Translation error: Unexpected response from Gemini."

            # Temporary server/rate-limit errors
            if response.status_code in [429, 500, 503, 504]:

                if attempt < max_retries - 1:

                    # Exponential backoff + small random delay
                    delay = (2 ** attempt) + random.uniform(0, 1)

                    time.sleep(delay)

                    continue

                return (
                    "Gemini is temporarily busy. "
                    "Please try again in a few seconds."
                )

            # Other errors
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get(
                    "message",
                    "Unknown API error"
                )

                return f"Translation error: {error_message}"

            except Exception:
                return (
                    f"Translation error: "
                    f"HTTP {response.status_code}"
                )

        except requests.exceptions.Timeout:

            if attempt < max_retries - 1:

                delay = (2 ** attempt) + random.uniform(0, 1)

                time.sleep(delay)

                continue

            return "Translation error: Request timed out. Please try again."

        except requests.exceptions.RequestException as e:

            if attempt < max_retries - 1:

                delay = (2 ** attempt) + random.uniform(0, 1)

                time.sleep(delay)

                continue

            return f"Translation error: {str(e)}"

        except Exception as e:

            return f"Translation error: {str(e)}"

    return "Translation error: Please try again."


# ---------------- GRADIO UI ----------------

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
        inputs=[
            text_input,
            source,
            target
        ],
        outputs=output
    )


# ---------------- LAUNCH APP ----------------

app.launch(
    server_name="0.0.0.0",
    server_port=int(
        os.environ.get("PORT", 7860)
    )
)