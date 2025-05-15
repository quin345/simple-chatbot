from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Your TinyLlama Docker API endpoint (adjust if different)
TINYLLAMA_API = "http://localhost:8000/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    # Forward the message to TinyLlama Docker API
    response = requests.post(
        TINYLLAMA_API,
        json={
            "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "messages": [{"role": "user", "content": user_message}]
        },
        headers={"Content-Type": "application/json"}
    )
    
    return jsonify({
        "reply": response.json()["choices"][0]["message"]["content"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
