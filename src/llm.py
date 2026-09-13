from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

apikey = os.getenv("GROQ_API_KEY")
client = Groq(api_key=apikey)

def generate_answer(prompt):

    response= client.chat.completions.create(
            messages = [
        {   "role":"user",
            "content": prompt
        }
        ],
        model = "openai/gpt-oss-20b",
        temperature=0.3
    )
    answer= response.choices[0].message.content
    return answer