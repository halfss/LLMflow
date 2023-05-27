import requests
import json

def send_sse_message(message):
    url = "http://localhost:7862/send-message"  # 替换为实际的 API URL

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=message)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")
        print("Response:", response.text)
