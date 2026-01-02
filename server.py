from flask import Flask, request, jsonify
import openai

openai.api_key = "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"

app = Flask(app)

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
    data = request.json
    mode = data["mode"]
    text = data["text"]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":PROMPTS[mode]},
            {"role":"user","content":text}
        ]
    )
    return jsonify({"result": response.choices[0].message.content})

app.run()
