import requests
import os
from groq import Groq

# URL für Browser https://www.reddit.com/r/Nachrichten/new/
url = "https://www.reddit.com/r/Nachrichten/new.json?limit=10"
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
news = ""

if response.status_code == 200:
    data = response.json()
    for post in data['data']['children']:
        title = post['data']['title']
        news = news + title + ". "
else:
    print("Fehler beim Abrufen der Daten. Statuscode:", response.status_code)

client = Groq(api_key=os.environ['GROQ_API_KEY'])
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Erstelle einen gut zu lesenden, interessanten Nachrichten Artikel in deutscher Sprache mit Fließtext zu den wichtigsten Punkten aus dieser Liste: " + news
        }
    ],
    temperature=1,
    max_tokens=7000,
    top_p=1,
    stream=False,
    stop=None,
)

print("\n\n")
print(completion.choices[0].message.content)
