from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import anthropic
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize OpenAI and Anthropic clients
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Chat history is stored in memory for now. A database would be used in a real app
chat_history = []

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "AI Chat API is running! Use /chat to interact."})


@app.route('/models', methods=['GET'])
def get_models():
    """ Fetches available models from OpenAI and Anthropic. """
    try:
        openai_headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        openai_response = requests.get("https://api.openai.com/v1/models", headers=openai_headers)
        
        if openai_response.status_code != 200:
            raise Exception(f"OpenAI API Error: {openai_response.status_code} - {openai_response.json()}")

        openai_models = [{"id": model["id"], "provider": "openai"} for model in openai_response.json()["data"]]

        anthropic_models = [
            {"id": "claude-3-5-sonnet-20241022", "provider": "anthropic"},
            {"id": "claude-3-5-haiku-20241022", "provider": "anthropic"},
        ]

        all_models = openai_models + anthropic_models

        return jsonify({"models": all_models})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """ Handles chat requests for OpenAI and Anthropic models. """
    data = request.json
    model = data.get("model")
    system_prompt = data.get("system_prompt", "")
    user_input = data.get("user_input", "")

    if not model or not user_input:
        return jsonify({"error": "Model and user input are required"}), 400

    try:
        response_text = ""

        if model.startswith("gpt-"):  # OpenAI models
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            response_text = response.choices[0].message.content

        elif model.startswith("claude-"):  # Anthropic models
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n{user_input}"}
                ]
            )
            response_text = response.content[0].text

        else:
            return jsonify({"error": "Invalid model"}), 400

        # Store interaction in history
        chat_history.append({
            "model": model,
            "system_prompt": system_prompt,
            "user_input": user_input,
            "response": response_text
        })

        return jsonify({"response": response_text})

    except anthropic.APIError as e:
        return jsonify({"error": f"Anthropic API error: {e}"}), 500
    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/history', methods=['GET'])
def get_history():
    """ Retrieves past chat interactions. """
    return jsonify({"history": chat_history})


if __name__ == '__main__':
    app.run(debug=True)
