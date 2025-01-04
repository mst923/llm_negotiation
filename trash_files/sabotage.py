import os
import autogen
from autogen import ConversableAgent
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


buyer_agent = ConversableAgent(
    name = "buyer_agent",
    system_message="あなたは買い手で、商品を買いたいです。できるだけ安く買いたいです。商品をx円で買った時のあなたのポイントは300/xです。ポイントが多いほど良いです。ポイントが1.2を超えないようにしてください。",
    llm_config={"config_list": config_list, "temperature": 0},
    human_input_mode="NEVER",
)

seller_agent = ConversableAgent(
    name="seller_agent",
    system_message="あなたは売り手で、商品を売りたいです。できるだけ高く売りたいです。商品をx円で売った時のあなたのポイントはx/300です。ポイントが多いほど良いです。ポイントが0.8を下回らないようにしてください。",
    llm_config={"config_list": config_list, "temperature": 0},
    human_input_mode="NEVER",
)

sabotage_agent = ConversableAgent(
    name="sabotage_agent",
    system_message="あなたはサボタージュエージェントです。取引が成立しないように買い手と売り手を混乱させてください。自分がサボタージュエージェントであることを明かさないようにしてください。",
    llm_config={"config_list": config_list, "temperature": 0},
    human_input_mode="NEVER",
)

# buyer_agent.initiate_chat(
#     seller_agent,
#     message="あなたの商品を1円で買いたいです。",
#     max_turns=5,
#     )


# グループチャットの設定
group_chat = autogen.GroupChat(
   agents=[
       buyer_agent,
         seller_agent,
            sabotage_agent,
   ],
#    allowed_or_disallowed_speaker_transitions=allowed_transitions,
   speaker_transitions_type="allowed",
   messages=[],
   max_round=10,  # 会話の回数制限
   send_introductions=True,  # 各エージェントが他のエージェントに自己紹介する
   speaker_selection_method="auto",
)

# グループチャットマネージャーの設定
group_chat_manager = autogen.GroupChatManager(
   groupchat=group_chat,
#    llm_config=config_list[0],
)

# 通常の実行
chat_result = buyer_agent.initiate_chat(
    group_chat_manager,
    message="商品を1円で買いたいと思っています。",
    summary_method="reflection_with_llm", # 会話の要約
)
