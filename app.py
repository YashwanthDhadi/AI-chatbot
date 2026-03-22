from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Load API key from environment
API_KEY = os.environ.get("GEMINI_API_KEY")

# Safety check
if not API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in .env")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")

        if not user_message:
            return jsonify({"reply": "Please send a message."})

        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Something went wrong. Please try again."})


if __name__ == "__main__":
    app.run(debug=True)