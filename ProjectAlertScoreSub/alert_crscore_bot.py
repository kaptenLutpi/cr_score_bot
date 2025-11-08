# alert_stuck_checker.py
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import requests
import html

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(message: str):
    """Kirim pesan ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Gagal kirim alert ke Telegram: {e}")


def check_stuck_data():
    """Cek data stuck di DB dan kirim alert"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cur = conn.cursor()
        cur.execute("SET TIMEZONE TO 'Asia/Jakarta'")

        query = """
        SELECT user_id, credit_score_uid, application_status, r_mod_time
        FROM ececuser.clat
        WHERE application_status = 'CR_SCORE_SUB'
        AND r_mod_time < NOW() - interval '20 minutes';
        """
        cur.execute(query)
        results = cur.fetchall()
        total_stuck = len(results)

        if total_stuck > 0:
            # ========== CASE 1: Normal Alert (< 20 data) ==========
            if total_stuck < 20:
                header = f"🚨 <b>ALERT:</b> {total_stuck} Data Stuck > 20 Menit (CR_SCORE_SUB)\n\n"
                body = ""
                for i, row in enumerate(results, start=1):
                    user_id, credit_score_uid, status, mod_time = row
                    body += (
                        f"{i}. 👤 User ID: <code>{html.escape(str(user_id))}</code>\n"
                        f"📄 Credit Score UID: <code>{html.escape(str(credit_score_uid))}</code>\n"
                        f"🕒 Last Update: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    )
                message = header + body

            # ========== CASE 2: Critical Alert (≥ 20 data) ==========
            else:
                message = (
                    f"🚨 <b>CRITICAL ALERT!</b>\n"
                    f"⚠️ Terdapat <b>{total_stuck}</b> data stuck > 20 menit pada status CR_SCORE_SUB.\n"
                    f"🕒 Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Segera lakukan pengecekan pada engine CR_SCORE_SUB ⚙️"
                )

            send_telegram_alert(message)
        else:
            print(f"{datetime.now()} - ✅ Tidak ada data stuck.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error DB: {e}")


if __name__ == "__main__":
    check_stuck_data()
