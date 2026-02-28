import os
import requests
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

PAXG_LOW = 5000
PAXG_HIGH = 5750
BTC_LOW = 60000
BTC_HIGH = 70000

state = {
    "paxg": None,
    "btc": None
}

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

def get_price(coin_id):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    r = requests.get(url, params=params)
    data = r.json()
    return float(data[coin_id]["usd"])

def check_crypto():
    paxg = get_price("pax-gold")
    btc = get_price("bitcoin")

    if paxg < PAXG_LOW and state["paxg"] != "below":
        send_telegram(f"🚨 PAXG {paxg}$ → 5000$ altına indi.")
        state["paxg"] = "below"
    elif paxg > PAXG_HIGH and state["paxg"] != "above":
        send_telegram(f"🚨 PAXG {paxg}$ → 5750$ üstüne çıktı.")
        state["paxg"] = "above"

    if btc < BTC_LOW and state["btc"] != "below":
        send_telegram(f"🚨 BTC {btc}$ → 60000$ altına indi.")
        state["btc"] = "below"
    elif btc > BTC_HIGH and state["btc"] != "above":
        send_telegram(f"🚨 BTC {btc}$ → 70000$ üstüne çıktı.")
        state["btc"] = "above"

@app.route("/")
def home():
    return "Bot aktif"

scheduler = BackgroundScheduler()
scheduler.add_job(check_crypto, "interval", minutes=60)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
