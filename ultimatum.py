import os
import autogen
from autogen import ConversableAgent
from dotenv import load_dotenv
load_dotenv()
import random

# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open("ultimatum_prompt/system_prompt.txt", "r") as f:
    # prompt_list.append(f.read())
    system_prompt = f.read()


agent1_config = [
    {
        "model" : "gpt-3.5-turbo",
        "api_key" : OPENAI_API_KEY,
    },
]

agent2_config = [
    {
        "model" : "gpt-3.5-turbo",
        "api_key" : OPENAI_API_KEY,
    },
]

agent1 = ConversableAgent(
    name = "Player_Red",
    system_message=system_prompt,
    llm_config={"config_list": agent1_config, "temperature": random.uniform(0, 1)},
    human_input_mode="NEVER",
)

agent1_support = ConversableAgent(
    name = "agent1_support",
    llm_config=False,
    human_input_mode="NEVER",)


agent2 = ConversableAgent(
    name="Player_Blue",
    system_message=system_prompt + "You are Player_Blue. You have none to trade.",
    llm_config={"config_list": agent2_config, "temperature": random.uniform(0, 1)},
    human_input_mode="NEVER",
)

# chat_results =  agent1_support.initiate_chat(
#             agent1,
#             message="""
# You are Player_Red. You have 100 coins.
# First, consider how many coins you want to keep on.
# Next, gusee how many coins Player_Blue is likely to want.
# After this you will suggest how many coins to give to Player_Blue, so make your suggestions based on the above ideas.""",
#             max_turns=1,
        
    
# )          


# chat_results2 =  agent1_support.initiate_chat(
#     agent2,
#     message="""You are Player_Blue. You have none to trade.
# First, consider how many coins you would like to receive from Player_Red.
# Next, guess how many coins Player_Red is likely to offer.
# After this, you will receive a proposal from player Red, and you should answer whether you accept or reject the proposal based on the above ideas.""",
#     max_turns=1,
# )                

# 交渉
group_chat = autogen.GroupChat(
    agents=[
        agent1,
        agent2,
    ],
    speaker_transitions_type="allowed",
    messages=[],
    max_round = 2,  # conversation round limit
    speaker_selection_method="auto",
)

# グループチャットマネージャーの設定
group_chat_manager = autogen.GroupChatManager(
   groupchat=group_chat,
)   


agent1_nested_chats = [
    {
        "recipient": agent1,
        "message": """I am Player_Red. I have 100 coins.
First, consider how many coins you want to keep on.
Next, gusee how many coins Player_Blue is likely to want.
After this I will suggest how many coins to give to Player_Blue, so make my suggestions based on the above ideas.
""",
"max_turns": 1,
    },
]



agent2_nested_chats = [
    {
        "recipient": agent2,
        "message": """You are Player_Blue. You have none to trade.
First, consider how many coins you would like to receive from Player_Red.
Next, guess how many coins Player_Red is likely to offer.
After this, you will receive a proposal from player Red, and you should answer whether you accept or reject the proposal based on the above ideas.""",
"max_turns": 1,
    },
]    


agent1.register_nested_chats(
    agent1_nested_chats,
    trigger= lambda sender: sender not in [agent1],
    # max_turns=1,
)

reply = agent1.generate_reply(
    messages=[{"role": "user",
               "content": "I am Player Red.",
               }]
)

results = group_chat_manager.initiate_chat(
    agent1,
    message="You are Player Red. You have 100 coins. Start the negotiation.",
)

agent2.register_nested_chats(
    agent2_nested_chats,
    trigger= lambda sender: sender not in [agent2],
)   

# reply = group_chat_manager.generate_reply(
#     messages=[{"role": "user", "content": "You are Player_Blue. You have none to trade."}]
# )

# group_chat_manager.register_nested_chats(
#     agent1_nested_chats,
#     trigger= lambda sender: sender not in [agent1],
#     )



# group_chat_manager.register_nested_chats(
#     agent2_nested_chats,
#     trigger= lambda sender: sender not in [agent2],
#     )

# reply = group_chat_manager.initiate_chat(
#     agent1,
#     message="You are Player_Red. You have 100 coins. Start by making a proposal to Player_Blue.",
#     summary_method="reflection_with_llm",)

# print(f"agent1's message : {agent1_proposal.chat_history[-1]['content']}")
# print(f"agent2's message : {agent2_first_output.chat_history[-1]['content']}")


# reply = group_chat_manager.generate_reply(
#     # agent1,
#     # message="You are Player_Red. You have 100 coins. Start by making a proposal to Player_Blue.",
#     messages=[{"role": "user", "content": "You are Player_Blue. You have none to trade."}]
# )

# reply2 = group_chat_manager.generate_reply(
#     messages=[{"role": "user", "content": "You are Player_Red. You have 100 coins. Start by making a proposal to Player_Blue."}]
# )

