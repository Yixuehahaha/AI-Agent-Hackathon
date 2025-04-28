import os
import streamlit as st

openai_api_key = os.getenv("OPENAI_API_KEY")

config_list = [
    {
        "model": "gpt-4o",
        "api_key": openai_api_key,
        "base_url": "https://api.openai.com/v1",
    }
]