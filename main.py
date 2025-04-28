import os
import re
from dotenv import load_dotenv
from prompts import CRITIC_PROMPT_TEMPLATE, REWRITE_PROMPT_TEMPLATE
from utils.image_checker import simple_image_check

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from agents.critic_agent import critic_agent
from agents.rewrite_agent import rewrite_agent

app = FastAPI()

def clean_critic_result(critic_text: str) -> str:
    if "Context Assumptions" in critic_text:
        idx = critic_text.find("Context Assumptions")
        critic_text = critic_text[:idx].strip()

    if critic_text:
        critic_text = re.sub(r"(\*\*)?\s*text critique\s*:?\s*(\*\*)?", "", critic_text, flags=re.IGNORECASE).strip()

    templates_to_remove = [
        "To provide a thorough analysis",
        "Based on the provided context, let's conduct a detailed audit",
        "However, I will outline a general framework"
    ]
    for template in templates_to_remove:
        if template in critic_text:
            idx = critic_text.find(template)
            critic_text = critic_text[:idx].strip()
            break

    return critic_text

@app.post("/cultura")
async def cultura_handler(
    text: str = Form(None),
    country: str = Form(...),
    language: str = Form(...),
    platform: str = Form(...),
    age: int = Form(None),
    gender: str = Form(None),
    income_level: str = Form(None),
    religion: str = Form(None),
    sensitive_contributors: str = Form(None),
    image_hint: str = Form(None),
    metadata: str = Form(None),
    image_file: UploadFile = File(None) 
):
    try:
        image_bytes = await image_file.read() if image_file else None

        result = run_pipeline(
            text=text,
            country=country,
            language=language,
            platform=platform,
            age=age,
            gender=gender,
            income_level=income_level,
            religion=religion,
            sensitive_contributors=sensitive_contributors,
            image_hint=image_hint,
            metadata=metadata,
            image_bytes=image_bytes 
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_pipeline(
    text: str,
    country: str,
    language: str,
    platform: str,
    age: int,
    gender: str,
    income_level: str,
    religion: str,
    sensitive_contributors: str,
    image_hint: str,
    metadata: str,
    image_bytes: bytes = None
) -> dict:
    """Run CulturaSense full pipeline from user input to critique and rewrite."""
    
    # check picture
    if image_bytes:
        try:
            image_analysis = simple_image_check(image_bytes, content_hint=image_hint)
        except Exception as e:
            image_analysis = f"Image analysis failed: {str(e)}"
    else:
        image_analysis = "No image uploaded." 
        

    # ========== Critic Prompt generation ==========
    if text and text.strip():  # raw copy
        critic_prompt = CRITIC_PROMPT_TEMPLATE.format(
            country=country,
            platform=platform,
            language=language,
            religion=religion,
            sensitive_contributors=sensitive_contributors,
            image_analysis=image_analysis,
            content=text,
            image_hint=image_hint or "No hint provided"
        )
    else:  # no raw copy, only picture
        critic_prompt = f"""
        Based on the uploaded image and hint, perform a cultural sensitivity audit.
        
        Context:
        - Country: {country}
        - Platform: {platform}
        - Language: {language}
        - Religion: {religion}
        - Sensitive Contributors: {sensitive_contributors}
        - Image Analysis: {image_analysis}
        - Image Hint: {image_hint or "No hint provided"}
        
        Instructions:
        - Identify cultural, religious, emotional risks in the image.
        - Suggest actionable improvements if needed.
        - Focus purely on visual aspects.
        """

    critic_result = critic_agent.generate_reply(
        messages=[{"role": "user", "content": critic_prompt}]
    )
    cleaned_critic_result = clean_critic_result(str(critic_result))

    # ========== Rewrite Prompt generation ==========
    rewrite_prompt = REWRITE_PROMPT_TEMPLATE.format(
        critique=critic_result,
        content=text
    )
    rewrite_result = rewrite_agent.generate_reply(
        messages=[{"role": "user", "content": rewrite_prompt}]
    )

    return {
        "critique": cleaned_critic_result,
        "rewritten_text": str(rewrite_result),
        "image_analysis": image_analysis or "No image uploaded."
    }

# CLI Debugging Portal (for local debugging)
if __name__ == "__main__":
    test_result = run_pipeline(
        text="This cream makes your skin white as snow!",
        country="Indonesia",
        language="Indonesian",
        platform="Shopee",
        age=25,
        gender="female",
        income_level="middle",
        religion="Islam",
        sensitive_contributors="skin tone, modesty",
        image_hint="",
        metadata="",
        image_bytes=None

    )

    print("\n Critique:\n", test_result["critique"])
    print("\n Rewritten Text:\n", test_result["rewritten_text"])
