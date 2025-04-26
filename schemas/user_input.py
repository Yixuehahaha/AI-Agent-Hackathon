from pydantic import BaseModel, Field
from typing import Optional, List

class UserInput(BaseModel):
    # Core content submitted by user
    text: Optional[str] = Field(None, description="Original textual content, optional")
    image_path: Optional[str] = Field(None, description="Path to uploaded image")
    pdf_path: Optional[str] = Field(None, description="Path to uploaded PDF file")

    # Geolocation and language context
    country: str = Field(..., description="Target country or region")
    language: str = Field(..., description="Preferred language")
    platform: str = Field(..., description="Target platform such as Shopee, TikTok, etc.")

    # Audience profile fields
    age: Optional[int] = Field(None, description="Age")
    gender: Optional[str] = Field(None, description="Gender")
    income_level: Optional[str] = Field(None, description="Income level")
    religion: Optional[str] = Field(None, description="Religious affiliation")
    disability_status: Optional[bool] = Field(False, description="Whether the user has a disability")

    # Cultural sensitivity input
    sensitive_contributors: Optional[str] = Field(None, description="Content or audience characteristics that require cultural sensitivity")
