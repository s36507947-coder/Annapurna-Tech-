from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# আপনার n8n Webhook URL এখানে বসাবেন
N8N_WEBHOOK_URL = "https://your-n8n-webhook-url.com/webhook/farmer-data"

@app.route('/submit-data', methods=['POST'])
def submit_data():
    try:
        content = request.json
        # n8n এ ডেটা পাঠানো হচ্ছে
        response = requests.post(N8N_WEBHOOK_URL, json=content)
        
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Data sent to n8n and Google Sheets!"}), 200
        else:
            return jsonify({"status": "error", "message": "n8n connection failed"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)