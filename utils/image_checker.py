# image_checker.py

import requests
import os
from dotenv import load_dotenv
load_dotenv()
# Read Azure configuration information from the .env file
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

def azure_image_analysis(image_bytes: bytes) -> str:
    """
        Call the Azure Computer Vision API to analyze images and return a natural language description.
        Input: Image byte stream
        Output: Short text description of image content
    """
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_VISION_KEY,
        "Content-Type": "application/octet-stream"
    }
    params = {
        "visualFeatures": "Description"
    }
    analyze_url = f"{AZURE_VISION_ENDPOINT}/vision/v3.2/analyze"

    try:
        response = requests.post(analyze_url, headers=headers, params=params, data=image_bytes)
        response.raise_for_status()
        result = response.json()

        if "description" in result and "captions" in result["description"]:
            captions = result["description"]["captions"]
            if captions:
                return captions[0]["text"]

        return "No obvious risks detected."

    except Exception as e:
        return f"Image Analysis Error: {str(e)}"

def simple_image_check(image, content_hint: str = None) -> str:
    if hasattr(image, "read"):
        image_bytes = image.read()
    else:
        image_bytes = image
        
    analysis_result = azure_image_analysis(image_bytes)

    combined_description = f"Azure Vision Description: {analysis_result}."

    if content_hint:
        combined_description += f" User provided hint: {content_hint}."

    return combined_description
