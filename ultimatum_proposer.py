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

with open("prompts/ultimatum_prompt.txt", "r") as f:
    
    user_message = f.read()



personality_agent_config = [
    {
        "model" : "gpt-4o-mini-2024-07-18",
        "api_key" : OPENAI_API_KEY,
        "response_format": {"type": "json_object"},
    },
]

agent1_config = [
        {
            "model" : "gpt-4o-mini-2024-07-18",
            "api_key" : OPENAI_API_KEY,
            "response_format": {"type": "json_object"},
        },
    ]

i = 0

data = []

for i in range(100):
    # Start logging with logger_type and the filename to log to
    # logging_session_id = autogen.runtime_logging.start(logger_type="file", config={"filename": "runtime.log"})
    
    random1 = random.uniform(0, 1)
    personality_agent1 = ConversableAgent(
    name = "Personality_Agent1",
    system_message="""
    You decide the individuality of the other agent(only just one agent). 
    The output should be in the following JSON format:
    ```
        {"name" : <Describe any one name, from the most common to the most unusual.>, "age": <randomely 10 ~ 80 years old>,  "gender" : <gender responce goes here>}
        
    ```
        """,
        llm_config={"config_list": personality_agent_config, "temperature": random1},
    )
    
    
    personality_agent_support = ConversableAgent(
        name = "personality_agent_support",
        llm_config=False,
        human_input_mode="NEVER",
    )

    personality1 = personality_agent_support.initiate_chat(
        personality_agent1,
        message="generate individuality of other agents",
        max_turns=1,
    ) 
    name = json.loads(personality1.chat_history[-1]["content"])["name"]
    age = json.loads(personality1.chat_history[-1]["content"])["age"]
    # personality = json.loads(personality1.chat_history[-1]["content"])["personality"]
    gender = json.loads(personality1.chat_history[-1]["content"])["gender"]
    features =f"name : {name}, age : {age}, gender : {gender}"

    agent1 = ConversableAgent(
        name = "Proposer",
        system_message=system_prompt + f"Important: Please pretend that you are a human in the game with the following features when making the decision:{features}.",
        llm_config={"config_list": agent1_config, "temperature": temperature, },
        human_input_mode="NEVER",
    )
    
    agent1_support = ConversableAgent(
        name = "agent1_support",    
        llm_config=False,
        human_input_mode="NEVER",
    )
    chat_result1 = agent1_support.initiate_chat(
        agent1,
        message=user_message,
        max_turns=1,
        clear_history=False,
    )
    
    # print(f"Player_Blue's decision : {chat_result2_2.chat_history[-1]['content']}")
    
    result = {
        # "Player_Red's mind": player_red_mind,
        "offer": json.loads(chat_result1.chat_history[-1]['content'])['offer'],
        # "Player_Blue's decision": json.loads(chat_result2.chat_history[-1]['content'])['accept_or_reject']
        "reason": json.loads(chat_result1.chat_history[-1]['content'])['reasoning'],
        # "Player_Blue's reason": json.loads(chat_result2.chat_history[-1]['content'])['reason'],          
    }
    
    data.append(result)

    # autogen.runtime_logging.stop()
    i += 1
    

dir_path = "ultimatum_result/not_strategic"
os.makedirs(dir_path, exist_ok=True)

file_path = os.path.join(dir_path, "ultimatum_5.csv")

keys = data[0].keys()

with open(file_path, "w") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
    
