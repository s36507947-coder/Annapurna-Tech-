from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# n8n Webhook URL (নিশ্চিত করুন এটি n8n-এ 'Production' এবং 'Active' করা আছে)
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # timeout=30 যোগ করা হয়েছে যাতে রেন্ডার সার্ভার বেশিক্ষণ অপেক্ষা করতে পারে
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message}, timeout=30)
        
        # n8n থেকে আসা আসল ডেটা প্রিন্ট করে দেখা (Render Logs-এ দেখতে পাবেন)
        print(f"n8n Status Code: {response.status_code}")
        print(f"n8n Response Text: {response.text}")

        if response.status_code == 200:
            data = response.json()
            # অনেক সময় n8n সরাসরি লিস্ট পাঠায়, তাই নিচের চেকটি জরুরি
            if isinstance(data, list) and len(data) > 0:
                ai_reply = data[0].get("output") or data[0].get("text")
            else:
                ai_reply = data.get("output") or data.get("text")
            
            if not ai_reply:
                ai_reply = "Ami ekhon uttor dite parchi na, n8n theke 'output' key asheni."
                
            return jsonify({"reply": ai_reply})
        
        else:
            # n8n যদি 500 দেয়, তার মানে সমস্যা n8n-এর ভেতরের সেটিংসে
            return jsonify({"reply": f"Error: n8n server issue (Status {response.status_code})"}), 500

    except requests.exceptions.Timeout:
        return jsonify({"reply": "Error: n8n server response timeout (khub deri hochhe)."}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"reply": "AI server-er sathe jogajog kora jachhe na."}), 500

if __name__ == '__main__':
    app.run(debug=True)