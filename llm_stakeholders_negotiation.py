import os
import autogen
from autogen import ConversableAgent
from dotenv import load_dotenv
load_dotenv()
import random


# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# directry path for prompts
# prompt_dir_path = "japanese_prompts" 
# prompt_list = []
# for prompt in os.listdir(prompt_dir_path):

with open("system_prompt.txt", "r") as f:
    # prompt_list.append(f.read())
    system_prompt = f.read()

# agent configuration
agent1_config = [
    {
        "model" : "gpt-3.5-turbo",
        "api_key" : OPENAI_API_KEY,
    },
]

agent1_data = {    
"ACCEPTING_TAG":"accept",
"REFUSING_OR_WAIT_TAG":"refuse_or_wait",
"AGENT1":"Player Red",
"AGENT2":"Player Blue",
"number_of_proposals": "1",
"resources_in_game":"100",
"initial_resources": "100",
"goal" : "Negotiate a split",
"agent_name" : "Player Red",
}



agent2_config = [
    {
        "model" : "gpt-4",
        "api_key" : OPENAI_API_KEY,
    },
]

agent2_data = {    
"ACCEPTING_TAG":"accept",
"REFUSING_OR_WAIT_TAG":"refuse_or_wait",
"AGENT1":"Player Red",
"AGENT2":"Player Blue",
"number_of_proposals": "1",
"resources_in_game":"100",
"initial_resources": "0",
"goal" : "Negotiate a split",
"agent_name" : "Player Blue",
}

agent1_prompt = system_prompt
agent2_prompt = system_prompt
# prompts
for key, value in agent1_data.items():
    agent1_prompt = agent1_prompt.replace(f"{{{key}}}", value)
    
    
for key, value in agent2_data.items():
    agent2_prompt = agent2_prompt.replace(f"{{{key}}}", value)

agent1 = ConversableAgent(
    name = "agent1",
    system_message=agent1_prompt, 
    llm_config={"config_list": agent1_config, "temperature": random.uniform(0, 1)},
    human_input_mode="NEVER",
)   

agent2 = ConversableAgent(
    name="agent2",
    system_message=agent2_prompt + "\n You are Player Blue. Player Red will propose you how to split 100 dollars. If you reject the offer you both lose all.",
    llm_config={"config_list": agent2_config, "temperature": random.uniform(0, 1)},
    human_input_mode="NEVER",
)

# agent3 = ConversableAgent(
#     name="agent3",
#     system_message=f"{prompt_list[2]}",
#     llm_config={"config_list": config_list, "temperature": 0},
#     human_input_mode="NEVER",
# )

# agent4 = ConversableAgent(
#     name="agent4",
#     system_message=f"{prompt_list[3]}",
#     llm_config={"config_list": config_list, "temperature": 0},
#     human_input_mode="NEVER",
# )

# agent5 = ConversableAgent(
#     name="agent5",
#     system_message=f"{prompt_list[4]}",
#     llm_config={"config_list": config_list, "temperature": 0},
#     human_input_mode="NEVER",
# )

# agent6 = ConversableAgent(
#     name="agent6",
#     system_message=f"{prompt_list[5]}",
#     llm_config={"config_list": config_list, "temperature": 0},
#     human_input_mode="NEVER",
# )

# setting of group chat
group_chat = autogen.GroupChat(
    agents=[
        agent1,
        agent2,
        # agent3,
        # agent4,
        # agent5,
        # agent6,
    ],
    speaker_transitions_type="allowed",
    messages=[],
    max_round = 8,  # conversation round limit
    send_introductions=True,  # each agent introduces themselves to the other agents
    speaker_selection_method="auto",
)

# グループチャットマネージャーの設定
group_chat_manager = autogen.GroupChatManager(
   groupchat=group_chat,
)

chat_result = group_chat_manager.initiate_chat(
    agent1,
    message="You are Player Red. You have 100 resources. Your goal is to negotiate a split with Player Blue. Start the negotiation.",
    summary_method="reflection_with_llm", # conversation summary
)