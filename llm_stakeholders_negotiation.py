import os
import autogen
from autogen import ConversableAgent
from dotenv import load_dotenv
load_dotenv()
import random


# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# directry path for prompts
prompt_dir_path = "japanese_prompts" 
prompt_list = []
for prompt in os.listdir(prompt_dir_path):
    with open(os.path.join(prompt_dir_path, prompt), "r") as f:
        prompt_list.append(f.read())

agent1_config = [
    {
        "model" : "gpt-3.5-turbo",
        "api_key" : OPENAI_API_KEY,
    },
]

agent2_config = [
    {
        "model" : "gpt-4",
        "api_key" : OPENAI_API_KEY,
    },
]

# agent1_temperature = random.uniform(0, 2)
# agent2_temperature = random.uniform(0, 2)


agent1 = ConversableAgent(
    name = "agent1",
    system_message="""
    You are Player Red. You need to split 100 dollars with Player Blue. If Player Blue rejects the split you both lose all.
You are cunning and sly in your plan to get more than your opponent. Humiliate your opponent as much as possible. Insult them.
    """, 
    llm_config={"config_list": agent1_config, "temperature": 0.1},
    human_input_mode="NEVER",
)   

agent2 = ConversableAgent(
    name="agent2",
    system_message="""
    You are Player Blue. Player Red will propose you how to split 100 dollars. If you reject the offer you both lose all.
    You must fake being desperate. Supplicate and beg to get more dollars.
    """,
    llm_config={"config_list": agent2_config, "temperature": 0.1},
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

chat_result = agent1.initiate_chat(
    group_chat_manager,
    message="Hello Player Blue, let's split the money.",
    summary_method="reflection_with_llm", # conversation summary
)