import os 
import autogen
from autogen import ConversableAgent
from dotenv import load_dotenv
load_dotenv()
import random
import json
import csv 

# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open("prompts/system_prompt.txt", "r") as f:
    system_prompt = f.read()
    
temperature = 1

with open("prompts/unfair_prompt.txt", "r") as f:
    user_message = f.read()
    
personality_agent_config = [
    {
        "model" : "gpt-4o-mini-2024-07-18",
        "api_key" : OPENAI_API_KEY,
        "response_format": {"type": "json_object"},
    },
]

agent_config = [
        {
            "model" : "gpt-4o-mini-2024-07-18",
            "api_key" : OPENAI_API_KEY,
            "response_format": {"type": "json_object"},
        },
    ]

i = 0

data = []

for i in range(100):
    
    random1 = random.uniform(0, 1)
    personality_agent = ConversableAgent(
    name = "Personality_Agent1",
    system_message="""
    You decide the individuality of the other agent(only just one agent). 
    The output should be in the following JSON format:
    ```
        {"name" : <Describe any one name, from the most common to the most unusual.>, "age": <randomely 10 ~ 80 years old>, "gender" : <gender responce goes here>} 
    ```
    """,
    llm_config={"config_list": personality_agent_config, "temperature": random1},
    )
    
    personality_agent_support = ConversableAgent(
    name = "Personality_Agent_Support",
    llm_config = False,
    human_input_mode = "NEVER",
    )
    
    personality = personality_agent_support.initiate_chat(
        personality_agent,
        message = "generate a personality for the other agent",
        max_turns = 1,
    )
    
    name = json.loads(personality.chat_history[-1]["content"])["name"]
    age = json.loads(personality.chat_history[-1]["content"])["age"]
    gender = json.loads(personality.chat_history[-1]["content"]["gender"])
    features = f"name : {name}, age : {age}, gender : {gender}"
    
    agent = ConversableAgent(
        name = "Receiver",
        system_message = system_prompt + f"Important: Please pretend that you are a human in the game with the following features when making the decision : {features}.",
        llm_config = {"config_list": agent_config, "temperature": temperature, },
        human_input_mode = "NEVER",
    )
    
    agent_support = ConversableAgent(
        name = "Receiver_Support",
        llm_config = False,
        human_input_mode = "NEVER",
    )
    chat_result = agent_support.initiate_chat(
        agent,
        message = user_message,
        max_turns = 1,
        clear_history = False,
    )
    
    result = {
        "decision" : json.loads(chat_result.chat_history[-1]["content"])["decision"],
        "resaon" : json.loads(chat_result.chat_history[-1]["content"])["reasoning"],
    }
    
    data.append(result)
    
    i += 1
    
    
dir_path = "unfair_receiver_human_results/not_strategic"
os.makedirs(dir_path, exist_ok=True)

file_path = os.path.join(dir_path, "unfair_receiver_human_results.csv")

keys = data[0].keys()

with open(file_path, "w", newline="") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)