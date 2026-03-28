from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Fetch n8n webhook URL from environment variables for security
# Apni Render-e 'N8N_WEBHOOK_URL' variable-ti set korben.
N8N_WEBHOOK_URL = os.environ.get('https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot')

if not N8N_WEBHOOK_URL:
    raise ValueError("N8N_WEBHOOK_URL environment variable is not set")

@app.route('/')
def index():
    """Serves the main chat application page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat messages. receives user input and forwards it to n8n."""
    # 1. Get user message from the frontend's POST request body
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 2. Prepare the data to send to n8n
        # The key name here ('message') must match what n8n's webhook node expects.
        # Check image_0.png - the webhook is set to GET. Change it to POST in n8n.
        data_to_n8n = {"message": user_message}
        
        # 3. Make the POST request to n8n's production webhook URL.
        # (Make sure to use the 'Production URL' from n8n)
        response = requests.post(N8N_WEBHOOK_URL, json=data_to_n8n)
        
        # 4. Process the response from n8n
        # n8n should respond with a JSON object.
        if response.status_code == 200:
            n8n_data = response.json()
            
            # Extract the AI's reply from n8n's JSON response.
            # We assume n8n sends the reply in a key called 'output'.
            # Configure 'Respond to Webhook' node in n8n to send this expression:
            # {{ { "output": $json.output } }}
            ai_reply = n8n_data.get("output", "I received a response but couldn't understand it.")
            
            # 5. Send the AI's reply back to the frontend
            return jsonify({"reply": ai_reply})
        else:
            return jsonify({"reply": f"n8n server error: {response.status_code}"}), 502

    except Exception as e:
        # Catch any other errors (e.g., connection issues)
        return jsonify({"reply": "I'm having trouble connecting to my brain. Please try again later."}), 500

if __name__ == '__main__':
    # Start the app in debug mode (only for local testing)
    app.run(debug=True)