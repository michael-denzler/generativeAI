import feedparser
import os
from bs4 import BeautifulSoup
from openai import OpenAI

client = OpenAI( api_key=os.environ['OPENAI_API_KEY'])
url = 'https://www.deutschlandfunk.de/nachrichten-100.rss'
feed = feedparser.parse(url)

news = "Es wird Ihnen präsentiert. Die aktuellsten Nachrichten vom Deutschlandfunk. Mein Name ist AI Mustermann. "

count = 0  # Zähler für die Anzahl der verarbeiteten Einträge
for entry in feed.entries:
    if count >= 5:
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

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="onyx",
    input=news,
) as response:
    response.stream_to_file("dlf_openai.mp3")
