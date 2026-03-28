from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# আপনার n8n Production Webhook URL
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get("message")
    
    if not user_message:
        return jsonify({"reply": "Kichu likhun..."}), 400

    try:
        # n8n-এ রিকোয়েস্ট পাঠানো হচ্ছে (timeout ৩০ সেকেন্ড দেওয়া হয়েছে)
        response = requests.post(
            N8N_WEBHOOK_URL, 
            json={"message": user_message}, 
            timeout=30 
        )
        
        # ডিবাগ করার জন্য প্রিন্ট (এটি রেন্ডার লগ-এ দেখা যাবে)
        print(f"Status: {response.status_code}, Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            
            # n8n আউটপুট ফরম্যাট চেক করা (লিস্ট বা ডিকশনারি)
            if isinstance(data, list) and len(data) > 0:
                ai_reply = data[0].get("output") or data[0].get("text")
            else:
                ai_reply = data.get("output") or data.get("text")
            
            if ai_reply:
                return jsonify({"reply": ai_reply})
            else:
                return jsonify({"reply": "n8n theke kono uttor pawa jayni."})
        
        else:
            return jsonify({"reply": f"Error: n8n error code {response.status_code}"}), 500

    except requests.exceptions.Timeout:
        return jsonify({"reply": "Server response korte deri korche, abar chesta korun."}), 500
    except Exception as e:
        print(f"System Error: {str(e)}")
        return jsonify({"reply": "AI server-er sathe jogajog hoyni."}), 500

if __name__ == '__main__':
    # রেন্ডারের পোর্টের সাথে খাপ খাওয়ানোর জন্য
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)