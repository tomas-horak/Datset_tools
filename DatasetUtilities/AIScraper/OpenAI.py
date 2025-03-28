import json
import os

from dotenv import load_dotenv
from openai import OpenAI


json_structure = {
            "name": "Název květiny XYZ",
            "scientific_name": "Vědecký název XYZ",
            "light_requirements": "Požadavky na světlo – př. Přímé sluneční světlo",
            "watering_instructions": "Požadavky na zalévání – př. 1 x týdně",
            "fertilization_instructions": "Požadavky na hnojení.",
            "soil_type": "Typ půdy",
            "common_issues": "Typické problémy a nemoci",
            "toxicity": "Zda je či není toxická pro zvířata či lidi",
            "sources": "Source example"
        }


json_string = json.dumps(json_structure)

if not load_dotenv():
    raise Exception("no .env file found")


api_key = os.environ.get("OPENAI_KEY")

client = OpenAI(api_key=api_key)

def get_plant_info(plant_name):
    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        web_search_options={"search_context_size": "medium"},
        messages=[{
            "role": "user",
            "content": f"Find info about correct care of {plant_name} houseplant."
                       f" Return the info in JSON format like this: {json_string}."
                       f" Return only the valid JSON. Put searched websites to sources key."
                       f" DO NOT wrap the output with JSON markers like ```json. "
        }]
    )
    return completion.choices[0].message.content

