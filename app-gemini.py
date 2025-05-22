from flask import Flask, request, jsonify, render_template
import requests
from config import GEMINI_API_KEY  # Import from separate file

app = Flask(__name__)

GEMINI_API = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    params = {
        "key": GEMINI_API_KEY  # Using API key as query parameter
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_message
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            GEMINI_API,
            params=params,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        
        # Extract the response text from Gemini's response structure
        gemini_response = response.json()
        reply = gemini_response['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)