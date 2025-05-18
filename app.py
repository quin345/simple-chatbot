from flask import Flask, request, jsonify, render_template
import requests
from config import DEEPSEEK_API_KEY  # Import from separate file

app = Flask(__name__)

DEEPSEEK_API = "https://api.deepseek.com/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"  # Use imported key
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(DEEPSEEK_API, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify({"reply": response.json()["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)