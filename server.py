from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

# Create Flask app
app = Flask(__name__)

# Enable CORS (for GitHub Pages / browser access)
CORS(app)

# OpenAI client (API key comes from Render environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt templates
PROMPTS = {
    "check": """You are an IAYP compliance checker.
Return:
OK:
MISSING:
NEEDS FIX:
Plain language only.""",

    "fill": """Fill missing IAYP diary parts.
Sound like a student.
Short sentences.
No exaggeration.""",

    "report": """Write a simple IAYP diary review.
Plain text.
No assessor mention."""
}

# Health check route
@app.route("/", methods=["GET"])
def health():
    return "IAYP Brain API is running"

# Main chat API route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)

    mode = data.get("mode")
    text = data.get("text")

    if mode not in PROMPTS or not text:
        return jsonify({"error": "Invalid mode or empty text"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PROMPTS[mode]},
            {"role": "user", "content": text}
        ]
    )

    return jsonify({
        "result": response.choices[0].message.content
    })
