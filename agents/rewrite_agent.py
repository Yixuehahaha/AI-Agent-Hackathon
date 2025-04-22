from autogen import ConversableAgent
from config.llm_config import config_list

rewrite_agent = ConversableAgent(
    name="RewriterAgent",
    system_message="""
    You are a copywriting expert focused on cultural adaptation. Based on previous feedback from the cultural sensitivity auditor,
    rewrite the user's original content to better align with the specified region's cultural norms, platform requirements,
    and audience characteristics. Maintain clarity, tone, and purpose, while ensuring cultural appropriateness.
    If the original input contains multiple languages, preserve or appropriately restructure them.
    """,
    llm_config={"config_list": config_list, "temperature": 0.7}
)