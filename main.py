from schemas.user_input import UserInput
from agents.critic_agent import critic_agent
from agents.rewrite_agent import rewrite_agent
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/cultura")
async def cultura_handler(user_input: UserInput):
    try:
        result = run_pipeline(user_input)  # Service层调用
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_pipeline(user_input: UserInput) -> dict:
    """Run CulturaSense full pipeline from user input to critique and rewrite."""

    # 1. Format prompt for CriticAgent
    critic_prompt = (
        f"Analyze this content for cultural sensitivity risks.\n"
        f"Context:\n"
        f"- Country: {user_input.country}\n"
        f"- Platform: {user_input.platform}\n"
        f"- Language: {user_input.language}\n"
        f"- Religion: {user_input.religion}\n"
        f"- Sensitive Contributors: {user_input.sensitive_contributors}\n\n"
        f"Content:\n{user_input.text}"
    )

    critic_result = critic_agent.generate_reply(
        messages=[{"role": "user", "content": critic_prompt}]
    )

    # 2. Format prompt for RewriterAgent
    rewrite_prompt = (
        f"Based on the following critique, rewrite the original content.\n"
        f"Critique:\n{critic_result}\n\n"
        f"Original:\n{user_input.text}"
    )

    rewrite_result = rewrite_agent.generate_reply(
        messages=[{"role": "user", "content": rewrite_prompt}]
    )

    return {
        "critique": str(critic_result),
        "rewritten_text": str(rewrite_result)
    }

# 🧪 CLI 调试入口
if __name__ == "__main__":
    test_input = UserInput(
        text="This cream makes your skin white as snow!",
        country="Indonesia",
        language="Indonesian",
        platform="Shopee",
        age=25,
        gender="female",
        income_level="middle",
        religion="Islam",
        sensitive_contributors="skin tone, modesty"
    )

    result = run_pipeline(test_input)
    print("\n🔍 Critique:\n", result["critique"])
    print("\n✍️ Rewritten Text:\n", result["rewritten_text"])
