import feedparser
import requests
import os
from bs4 import BeautifulSoup
from openai import OpenAI


client = OpenAI( api_key=os.environ['OPENAI_API_KEY'])
url = 'https://www.deutschlandfunk.de/nachrichten-100.rss'
feed = feedparser.parse(url)

news = "Es wird Ihnen präsentiert. Die aktuellsten Nachrichten vom Deutschlandfunk. Mein Name ist AI Mustermann. "

count = 0  # Zähler für die Anzahl der verarbeiteten Einträge
for entry in feed.entries:
    if count >= 3:
        break  # Stoppe die Schleife, wenn 10 Einträge verarbeitet wurden

    title = entry.title
    description = entry.description
    
    # Bereinige den HTML-Text aus der Beschreibung
    soup = BeautifulSoup(description, 'html.parser')
    cleaned_description = soup.get_text()
    
    print(title + ": " + cleaned_description)
    print("\n")

    news = news + "\n" + title + ": " + cleaned_description
    count += 1  # Erhöhe den Zähler nach Verarbeitung eines Eintrags

news = news + "\n Das waren die Nachrichten. Ich übergebe zurück zu Michael!"

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/5rYKbE3tiK3Rwxxd2Zr6"
#url = "https://api.elevenlabs.io/v1/text-to-speech/w2qZgZJbxOuKVruWuVU1"


headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": os.environ['ELEVEN_API_KEY']
}

data = {
  "text": news,
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('dlf_11labs.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
