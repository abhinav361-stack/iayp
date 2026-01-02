from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mode = data.get("mode")
    text = data.get("text")

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
