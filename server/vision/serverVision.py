import base64
import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Headers for the OpenAI API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # Get the JSON payload from the request
        data = request.get_json()

        # Extract the base64 image data
        base64_image = data.get('image')

        if not base64_image:
            return jsonify({"error": "No image data provided"}), 400

        # Prepare the payload for the OpenAI API request
        payload = {
            "model": "gpt-4o-mini",  # Replace with the correct model name
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Detect to me whether or not you see a red ball. Only say YES or NO."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Send the request to the OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()

        # Extract the message content from the response
        message = response_json['choices'][0]['message']['content']

        # Check if the message contains any "off" keywords
        off_keywords = ["unusual", "off", "weird", "strange", "surreal", "disconnection", "odd"]
        is_off = any(keyword in message.lower() for keyword in off_keywords)

        return jsonify({
            "message": message,
            "is_off": is_off,
            "full_response": response_json
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)