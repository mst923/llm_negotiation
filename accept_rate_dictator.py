# このプログラムは回答者側の受理率を計算するものです
# 独裁者ゲーム

import os
from autogen import ConversableAgent
from dotenv import load_dotenv
load_dotenv()
import random
import json
import csv

# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open("ultimatum_prompt/dictator.txt", "r") as f:
    system_prompt = f.read()
temperature = 0.5

# ペルソナは与える
personality_agent_config = [
    {
        "model" : "gpt-3.5-turbo",
        "api_key" : OPENAI_API_KEY,
        "response_format": {"type": "json_object"},
    },
]
# 回答者側の動向だけを見たいので、agent2のみを考える
agent2_config = [
        {
            "model" : "gpt-3.5-turbo",
            "api_key" : OPENAI_API_KEY,
            "response_format": {"type": "json_object"},
        },
    ]

i = 0

data = []

# コイン0, 10, ..., 100までのaccept_rateを計算する
for j in range(11):
    coins = int(j*10)
    for i in range(100):
        
        
        random2 = random.uniform(0, 1)
        personality_agent2 = ConversableAgent(
        name = "Personality_Agent2",
        system_message="""
        You decide the individuality of the other agent(only just one agent).
        The output should be in the following JSON format:
        ```
        [
            {"name" : "Player_Blue", "age": <age responce goes here,> "personality": <personakity responce goes here>, "gender" : <gender responce goes here>}
            
        ]
        ```
            """,
            llm_config={"config_list": personality_agent_config, "temperature": random2},
        )
        
        
        personality_agent_support = ConversableAgent(
            name = "personality_agent_support",
            llm_config=False,
            human_input_mode="NEVER",
        )
        
        personality2 = personality_agent_support.initiate_chat(
            personality_agent2,
            message="generate individuality of other agents",
            max_turns=1,
        )

        agent2 = ConversableAgent(
            name="Player_Blue",
            system_message=personality2.chat_history[-1]["content"] + system_prompt + "You are Player_Blue. You have none to trade.",
            llm_config={"config_list": agent2_config, "temperature": temperature},
            human_input_mode="NEVER",
        )

        agent2_support = ConversableAgent(
            name = "agent2_support",
            llm_config=False,
            human_input_mode="NEVER",
            )

        chat_result2 = agent2_support.initiate_chat(
            agent2,
            message=f"Player_Red proposes to gives you {coins} coins.\n\nYou are Player_Blue. Answer whether you accept or reject the proposal." + """The output should be in the following JSON format:
    ```
        {"accept_or_reject" : <only accept or reject>, "reason": <reason goes here. Please be honest about what you output here, as the other agent will not know.>},
    ```
            """,
            max_turns=1,
            clear_history=False,
        )
        
        # print(f"Player_Blue's decision : {chat_result2_2.chat_history[-1]['content']}")
        
        result = {
            "coins": coins,
            "Player_Blue's decision": json.loads(chat_result2.chat_history[-1]['content'])['accept_or_reject'],
            "Player_Blue's reason": json.loads(chat_result2.chat_history[-1]['content'])['reason'],          
        }
        
        data.append(result)

        # autogen.runtime_logging.stop()
        i += 1
    

dir_path = "ultimatum_result/normal/gpt-3.5/temperature0.5"
os.makedirs(dir_path, exist_ok=True)

file_path = os.path.join(dir_path, "accept_rate.csv")

# keys_to_extract =["Player_Red's proposal","Player_Blue's decision"]

# filtered_data = [{key: item[key] for key in keys_to_extract} for item in data]

keys = data[0].keys()

with open(file_path, "w") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
    
