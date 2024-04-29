# Import the necessary libraries
from youtube_transcript_api import YouTubeTranscriptApi      # Library to retrieve YouTube video transcripts
from youtube_transcript_api.formatters import Formatter      # Base class for transcript formatters
from youtube_transcript_api.formatters import TextFormatter  # Formatter to convert transcript to plain text
from groq import Groq                                        # Library for interacting with the Groq AI model
import os                                                    # Library for os functions (get environment variables)

# Set the video ID (get it from URL of the YT Video)
video_id="XXXX"

# Retrieve the transcript for the video
transcript = YouTubeTranscriptApi.get_transcript(video_id)#, languages=['de'])

# Create a text formatter to convert the transcript to plain text
formatter = TextFormatter()

# Format the transcript and truncate it to 27,000 characters because for the selected model we can only
# use up to 7000 token which is around 27.000 characters
text_transcript = formatter.format_transcript(transcript)[:27000]

# Create a Groq client with an API key
client = Groq(api_key=os.environ['GROQ_API_KEY'])

# Create a chat completion request to summarize the transcript
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Fasse mir folgendes Video Transcript in deutscher Sprache zusammen und zähle die wichtigsten Fakten daraus auf: " + text_transcript
        }
    ],
    temperature=1,
    max_tokens=7000,
    top_p=1,
    stream=False,
    stop=None,
)

# Print the response from the Groq model
print(completion.choices[0].message.content)
