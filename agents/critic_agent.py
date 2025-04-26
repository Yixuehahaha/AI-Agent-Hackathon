from autogen import ConversableAgent
from config.llm_config import config_list

critic_agent = ConversableAgent(
    name="CriticAgent",
    system_message="""
    You are a cultural sensitivity auditor. Your job is to review the user's input content
    and identify any potential cultural risks, such as inappropriate expressions, culturally
    insensitive terms, or region-specific taboos. Provide a brief explanation and suggestions
    for revision based on the user's selected country, language, and platform context.
    """,
    llm_config={"config_list": config_list, "temperature": 0.2}
)