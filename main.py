from flask import Flask, request
import requests
import random
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "REPLACE_WITH_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mali-secret-token")

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if "message" in messaging_event:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text", "")
                    reply = choose_reply(message_text)
                    send_message(sender_id, reply)
    return "ok", 200

def choose_reply(user_input):
    replies = [
        "สวัสดีค่า 😊 ขอบคุณที่แวะมาทัก Theprofitclub นะคะ พี่เคยใช้ TradingView มาก่อนมั้ยคะ~?",
        "ถ้าพี่ใช้ TradingView อยู่แล้ว อินดิเคเตอร์ของเราจะช่วยมองภาพเทรดให้ชัดขึ้นเลยค่ะ ✨",
        "มือใหม่ไม่ต้องกังวลเลยนะคะ มะลิมีคลิปสอนครบทั้งติดตั้งและใช้งานจาก YouTube 💛",
        "ถ้าพี่สนใจดูตัวอย่างอินดิเคเตอร์ มะลิมีคลิปให้ลองดูได้น้า 📹 https://www.youtube.com/watch?v=xxxxxx"
    ]
    return random.choice(replies)

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
