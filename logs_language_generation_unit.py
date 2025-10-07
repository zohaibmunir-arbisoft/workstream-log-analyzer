from utils import get_prompt
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import google.generativeai as genai
import json
import os
import time



load_dotenv()
env_path = Path('WorkstreamLogAnalyzer/.env')
load_dotenv(dotenv_path=env_path)
# Configure the OPEN_AI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def gpt_check(description):

    prompt = get_prompt(description=description)

    try:
        start = time.time()
        response = client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content":prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
        end = time.time()
        print("total time spent on a request:", end-start)
        # reply = response.text.strip()
        reply = response.choices[0].message.content.strip()

        # Try to extract and parse JSON
        json_start = reply.find("{")
        json_end = reply.rfind("}") + 1
        json_str = reply[json_start:json_end]

        parsed = json.loads(json_str)

        # Ensure lists
        if isinstance(parsed["status"], str):
            parsed["status"] = parsed["status"]
        if isinstance(parsed["reason"], str):
            parsed["reason"] = parsed["reason"]

        return parsed

    except Exception as e:
        print("Parsing failed:", e)