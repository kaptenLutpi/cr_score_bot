import schedule
import time
import logging
from datetime import datetime
from alert_crscore_bot import check_stuck_data, send_telegram_alert  # pastikan fungsi ini ada

# 📝 Setup logging
logging.basicConfig(
    filename="alert_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

START_HOUR = 8   # jam mulai aktif
END_HOUR = 20    # jam berhenti aktif
BOT_ACTIVE = False  # status awal bot

def job():
    global BOT_ACTIVE
    now = datetime.now()
    current_hour = now.hour

    # 🕗 Saat jam aktif
    if START_HOUR <= current_hour < END_HOUR:
        # Jika sebelumnya bot belum aktif (baru nyala pagi ini)
        if not BOT_ACTIVE:
            send_telegram_alert("☀️ <b>Bot aktif kembali</b> — pengecekan data dimulai.")
            BOT_ACTIVE = True

        print(f"⏳ [{now}] Menjalankan pengecekan data stuck...")
        logging.info("Menjalankan pengecekan data stuck...")
        try:
            check_stuck_data()
        except Exception as e:
            logging.error(f"❌ Error saat menjalankan job: {e}")
            print(f"❌ Error saat menjalankan job: {e}")

    # 🌙 Saat jam non-aktif
    else:
        if BOT_ACTIVE:
            send_telegram_alert("🌙 <b>Bot berhenti sementara</b> — di luar jam kerja (08:00–20:00).")
            BOT_ACTIVE = False
        print(f"🌙 [{now}] Di luar jam kerja. Bot tidak aktif.")
        logging.info("Di luar jam kerja. Bot tidak aktif.")

# Jalankan setiap 15 menit
schedule.every(15).minutes.do(job)

print(f"✅ Scheduler aktif. Bot akan cek data setiap 15 menit antara jam {START_HOUR}:00 - {END_HOUR}:00.")
logging.info(f"Scheduler aktif. Bot berjalan setiap 15 menit antara jam {START_HOUR}:00 - {END_HOUR}:00.")

# 🔁 Loop utama
while True:
    schedule.run_pending()
    time.sleep(1)
