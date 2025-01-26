from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import anthropic
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize OpenAI and Anthropic clients
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route('/', methods=['GET'])
def home():
    """
    Home route to verify that the API is running.
    """
    return jsonify({"message": "AI Chat API is running!"})


@app.route('/models', methods=['GET'])
def get_models():
    """
    Fetches and returns available AI models from OpenAI and Anthropic.
    """
    try:
        # Fetch OpenAI models
        openai_headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        openai_response = requests.get("https://api.openai.com/v1/models", headers=openai_headers)
        
        if openai_response.status_code != 200:
            raise Exception(f"OpenAI API Error: {openai_response.status_code} - {openai_response.json()}")

        openai_models = [{"id": model["id"], "provider": "openai"} for model in openai_response.json()["data"]]

        # List of supported Anthropic models
        anthropic_models = [
            {"id": "claude-3-5-sonnet-20241022", "provider": "anthropic"},
            {"id": "claude-3-5-haiku-20241022", "provider": "anthropic"},
        ]

        # Combine both OpenAI and Anthropic models
        all_models = openai_models + anthropic_models

        return jsonify({"models": all_models})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles chat requests, forwarding input to either OpenAI or Anthropic based on the selected model.
    """
    data = request.json
    model = data.get("model")
    system_prompt = data.get("system_prompt", "")
    user_input = data.get("user_input", "")

    # Validate request payload
    if not model or not user_input:
        return jsonify({"error": "Model and user input are required"}), 400

    try:
        if model.startswith("gpt-"):  # OpenAI models
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            return jsonify({"response": response.choices[0].message.content})

        elif model.startswith("claude-"):  # Anthropic models
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n{user_input}"}
                ]
            )
            return jsonify({"response": response.content[0].text})

        else:
            return jsonify({"error": "Invalid model"}), 400

    except anthropic.APIError as e:
        return jsonify({"error": f"Anthropic API error: {e}"}), 500
    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
