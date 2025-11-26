import time
import feedparser
from telegram import Bot

BOT_TOKEN = "TON_NOUVEAU_TOKEN_ICI"  # mets ici le NOUVEAU token (sans me le montrer)
CHAT_ID = TON_CHAT_ID_ICI            # remplace par ton chat_id numérique (ex: 123456789)
CHECK_INTERVAL = 60  # toutes les 60 secondes

KEYWORDS = [
    "ukraine",
    "ceasefire",
    "peace plan",
    "peace deal",
    "trump",
    "zelensky",
    "kyiv",
    "russia",
    "negotiation",
    "treaty",
    "putin",
]

FEEDS = [
    "https://feeds.reuters.com/reuters/worldNews",
    "https://feeds.reuters.com/reuters/topNews",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
]

bot = Bot(token=BOT_TOKEN)
seen_entries = set()

def match_kw(text):
    text = text.lower()
    return any(kw in text for kw in KEYWORDS)

def check_feeds():
    for url in FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            uid = e.get("id", e.get("link"))
            if uid in seen_entries:
                continue

            title = e.get("title", "")
            summary = e.get("summary", "")
            link = e.get("link", "")

            combined = f"{title} {summary}"

            if match_kw(combined):
                msg = f"📰 *ALERTE NEWS*\n\n*{title}*\n{summary}\n\n🔗 {link}"
                bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

            seen_entries.add(uid)

def main():
    print("Bot news lancé.")
    while True:
        try:
            check_feeds()
        except Exception as ex:
            print("Erreur:", ex)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
