import os

import pandas as pd
import json


def get_data():
    file_path = './dataset/project_task_day_details_2025.csv'
    df = pd.read_csv(file_path)
    return df

def get_prompt(logs):
    file_path = "prompts.json"

    with open(file_path, 'r') as file:
        # Load the JSON data from the file into a Python object (e.g., dictionary or list)
        messages = json.load(file)
    prompt = messages['prompt_for_description_check'].format(logs=logs)

    return prompt





