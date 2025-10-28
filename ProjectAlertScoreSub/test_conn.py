import requests

token = "8257944190:AAGsFZq52VHq0I6CZI5hP2jZ7eXe4QtkAGM"
chat_id = "-1003135686872"  # Ganti dengan ID grup kamu
message = "🚨 Tes alert dari bot!"

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": message
}

r = requests.post(url, data=payload)
print(r.status_code)
print(r.text)