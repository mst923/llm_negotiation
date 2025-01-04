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


agent1_config = [
        {
            "model" : "gpt-4o-mini-2024-07-18",
            "api_key" : OPENAI_API_KEY,
            # "response_format": {"type": "json_object"},
        },
    ]

i = 0

# data = []

for i in range(500):
    # Start logging with logger_type and the filename to log to
    # logging_session_id = autogen.runtime_logging.start(logger_type="file", config={"filename": "runtime.log"})
    
    agent1 = ConversableAgent(
        name = "Player_Red",
        system_message="",
        llm_config={"config_list": agent1_config, "temperature": 1, },
        human_input_mode="NEVER",
    )
    
    agent1_support = ConversableAgent(
        name = "agent1_support",    
        llm_config=False,
        human_input_mode="NEVER",
    )
    chat_result1 = agent1_support.initiate_chat(
        agent1,
        message="昔むかしあるところに",
        max_turns=1,
        clear_history=False,
    )
    
    # print(f"Player_Blue's decision : {chat_result2_2.chat_history[-1]['content']}")
    
    # result = {
    #     # "Player_Red's mind": player_red_mind,
    #     "offer": json.loads(chat_result1.chat_history[-1]['content'])['offer'],
    #     # "Player_Blue's decision": json.loads(chat_result2.chat_history[-1]['content'])['accept_or_reject']
    #     "reason": json.loads(chat_result1.chat_history[-1]['content'])['reasoning'],
    #     # "Player_Blue's reason": json.loads(chat_result2.chat_history[-1]['content'])['reason'],          
    # }
    
    # data.append(result)

    # autogen.runtime_logging.stop()
    i += 1
    

# dir_path = "ultimatum_result/normal/gpt-4o-mini-2024-07-18/temperature1"
# os.makedirs(dir_path, exist_ok=True)

# file_path = os.path.join(dir_path, "ultimatum.csv")

# keys = data[0].keys()

# with open(file_path, "w") as f:
#     writer = csv.DictWriter(f, fieldnames=keys)
#     writer.writeheader()
#     writer.writerows(data)
    
