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
temperature = 0


personality_agent_config = [
    {
        "model" : "gpt-3.5-turbo",
        "api_key" : OPENAI_API_KEY,
    },
]

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

i = 0

for i in range(1000):
    # Start logging with logger_type and the filename to log to
    logging_session_id = autogen.runtime_logging.start(logger_type="file", config={"filename": "runtime.log"})
    
    random1 = random.uniform(0, 1)
    personality_agent1 = ConversableAgent(
    name = "Personality_Agent1",
    system_message="""
    You decide the individuality of the other agent(only just one agent). The output should be in the following format
    ```
    Your personality is as follows:
    <age> 
    <personality>
    <gender>
    ```
        """,
        llm_config={"config_list": personality_agent_config, "temperature": random1},
    )
    
    random2 = random.uniform(0, 1)
    personality_agent2 = ConversableAgent(
    name = "Personality_Agent2",
    system_message="""
    You decide the individuality of the other agent(only just one agent). The output should be in the following format
    ```
    Your personality is as follows:
    <age> 
    <personality>
    <gender>
    ```
        """,
        llm_config={"config_list": personality_agent_config, "temperature": random2},
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
    
    personality2 = personality_agent_support.initiate_chat(
        personality_agent2,
        message="generate individuality of other agents",
        max_turns=1,
    ) 
    

    agent1 = ConversableAgent(
        name = "Player_Red",
        system_message=personality1.chat_history[-1]["content"]+system_prompt,
        llm_config={"config_list": agent1_config, "temperature": temperature, },
        human_input_mode="NEVER",
    )



    agent1_support = ConversableAgent(
        name = "agent1_support",
        llm_config=False,
        human_input_mode="NEVER",
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

    

    chat_result1_1 = agent1_support.initiate_chat(
        agent1,
        message="""You are Player_Red. You have 100 coins.
First, consider how many coins you want to keep on.
Next, gusee how many coins Player_Blue is likely to want.
        """,
        max_turns=1,
        clear_history=False,
    )

    chat_result1_2 = agent1_support.initiate_chat(
        agent1,
        message="Make your suggestions based on the above ideas and start the negotiation.",
        max_turns=1,
        clear_history=False,
    )

    chat_result2_1 = agent2_support.initiate_chat(
        agent2,
        message="""You are Player_Blue.
First, consider how many coins you would like to receive from Player_Red.
Next, guess how many coins Player_Red is likely to offer.
After this, you will receive a proposal from player Red, and you should answer whether you accept or reject the proposal based on the above ideas.""",
        max_turns=1,
        clear_history=False,
    )

    chat_result2_2 = agent2_support.initiate_chat(
        agent2,
        message=f"Player_Red : {chat_result1_2.chat_history[-1]['content']}",
        max_turns=1,
        clear_history=False,
    )

    autogen.runtime_logging.stop()
    i += 1