import os
from openai import OpenAI
import requests

# Setzen Sie hier Ihren OpenAI API Schlüssel ein
api_key = os.environ['OPENAI_API_KEY']

# Bild-URL, das Sie analysieren möchten
image_url = 'https://github.com/michael-denzler/generativeAI/blob/main/example.png?raw=true'

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Was ist auf diesem Bild zu sehen?"},
        {
          "type": "image_url",
          "image_url": {
            "url": image_url,
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])
