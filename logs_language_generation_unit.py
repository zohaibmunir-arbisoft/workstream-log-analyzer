from utils import get_prompt
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import json
import os
import time
from schema import LogsValidationResults


load_dotenv()
env_path = Path('WorkstreamLogAnalyzer/.env')
load_dotenv(dotenv_path=env_path)
# Configure the OPEN_AI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def gpt_check(logs):

    prompt = get_prompt(logs=logs)
    try:
        response = client.chat.completions.parse(
            model="gpt-4.1-mini",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content":prompt},
            ],
            temperature=0.7,
            response_format=LogsValidationResults
        )
        return response.choices[0].message.parsed

    except Exception as e:
        print("Parsing failed:", e)