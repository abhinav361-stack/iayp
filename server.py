from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq client (FREE, no billing)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

@app.route("/", methods=["GET"])
def health():
    return "IAYP Brain API (FREE – Groq) is running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    mode = data.get("mode")
    text = data.get("text")

    if mode not in PROMPTS or not text:
        return jsonify({"error": "Invalid mode or empty text"}), 400

    response = client.chat.completions.create(
        model="Llama 3.3 70B Versatile",

        messages=[
            {"role": "system", "content": PROMPTS[mode]},
            {"role": "user", "content": text}
        ]
    )

    return jsonify({
        "result": response.choices[0].message.content
    })


