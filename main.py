import autogen
import os
from dotenv import load_dotenv
load_dotenv()

# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config_list = [
    {
        "model" : "gpt-4",
        "api_key" : OPENAI_API_KEY,
    },
]


# create an AssistantAgent named "assistant"

assistant = autogen.AssistantAgent(

    name="assistant",

    llm_config={

        "seed": 42,  # seed for caching and reproducibility

        "config_list": config_list,  # a list of OpenAI API configurations

        "temperature": 0,  # temperature for sampling

    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API

)

# create a UserProxyAgent instance named "user_proxy"

user_proxy = autogen.UserProxyAgent(

    name="user_proxy",

    human_input_mode="NEVER",

    max_consecutive_auto_reply=10,

    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),

    code_execution_config={

        "work_dir": "coding",

        "use_docker": False,  # set to True or image name like "python:3" to use docker

    },

)

# the assistant receives a message from the user_proxy, which contains the task description

user_proxy.initiate_chat(

    assistant,

    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",

)

# followup of the previous question

user_proxy.send(

    recipient=assistant,

    message="""Plot a chart of their stock price change YTD and save to stock_price_ytd.png.""",

)