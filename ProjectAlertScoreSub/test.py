import requests

token = "8257944190:AAGsFZq52VHq0I6CZI5hP2jZ7eXe4QtkAGM"
chat_id = "6004522574"  # atau ganti dengan ID grup kamu
text = "🔔 Tes alert dari bot (manual test)"

r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": text})
print(r.status_code, r.text)
