import json
import os
import httpx

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), http_client=httpx.Client(verify=False))

# Function to generate encounter
def generate_encounter(level_range, difficulty, biome, context):
    """
    Returns a json object containing the AI for the encounter
    """
    prompt = generate_ai_prompt(level_range, difficulty, biome, context)
    model = "gpt-4o"

    print(f"Generating AI response using {model}... Please Wait.")
    response = client.chat.completions.create(
    model= model,
    response_format={ "type": "json_object" },
    temperature=.8,
    messages=[
        {"role": "user", "content": prompt}
        ]
    )
    text_response = response.choices[0].message.content

    try:
        json_response = json.loads(text_response)
        return json_response
    except json.JSONDecodeError:
        print("Failed to decode JSON from model response.")
        return None

def generate_ai_prompt(level_range, difficulty, biome, context):
    """Returns a string containing a prompt for the AI to generate an encounter"""
    return f"""
        Generate a Pathfinder 2e encounter in JSON format based on the following parameters:
        - Level Range: {level_range}
        - Difficulty: {difficulty}
        - Biome: {biome}
        - Context: {context}
        
        The encounter should be terse and to the point, leaning on sense verbs to provide players with a vivid experience. 
        The monsters must exist and have a link on https://2e.aonprd.com/Monsters.aspx 
        You must be accurate on these links.
        
        Response Format:
        {{
            "monster_links": [
                {{"name": "monster_name_1", "link": "https://2e.aonprd.com/Monsters.aspx/ID=(id of monster)"}},
                {{"name": "monster_name_2", "link": "https://2e.aonprd.com/Monsters.aspx/ID=(id of monster)"}},
                ...
            ],
            "description": "A detailed description of the encounter, with monster names matching those listed in 'monster_links'"
        }}

        Ensure that the names in "monster_links" match exactly with how they appear in the description.
        """