import json
import base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_code():
    if 'image' not in request.files or 'prompt' not in request.form:
        return jsonify({"error": "Missing image or prompt"}), 400

    image = request.files['image']
    prompt = request.form.get('prompt')  # Receive full prompt directly from Tkinter

    # Convert image to Base64 (in-memory)
    image_bytes = image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Send request to OpenAI GPT-4 Vision
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are an expert UI/UX developer."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},  # Use the exact prompt from Tkinter
                    {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
                ]}
            ],
            max_tokens=1000
        )

        ai_output = response["choices"][0]["message"]["content"]

        # Extract HTML & CSS
        html_code, css_code = ai_output.split("```css")
        html_code = html_code.replace("```html", "").strip()
        css_code = css_code.replace("```", "").strip()

        return jsonify({"html": html_code, "css": css_code})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)