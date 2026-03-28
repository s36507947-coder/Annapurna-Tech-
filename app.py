from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Apnar n8n Production Webhook URL
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    # Eti templates/index.html file-ti show korbe
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Frontend theke user-er message-ti neowa hochhe
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # n8n-e POST request pathano hochhe
        # n8n AI Agent-e apni {{ $json.body.message }} diye eti access korben
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message})
        
        if response.status_code == 200:
            data = response.json()
            # n8n theke asha 'output' key-ti frontend-e pathano hochhe
            ai_reply = data.get("output", "Sorry, I couldn't process the response.")
            return jsonify({"reply": ai_reply})
        else:
            return jsonify({"reply": f"Error: n8n returned status {response.status_code}"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"reply": "Error connecting to AI server."}), 500

if __name__ == '__main__':
    app.run(debug=True)