# file: api_gemini.py
import os
from fastapi import HTTPException
from google import genai

API_KEY = os.environ.get("API_KEY")


def ask_gemini_baking(question: str) -> str:
    # 1. בדיקה שהמפתח מוגדר בשרת
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY is missing in environment variables",
        )

    try:
        # 2. חיבור ל-Google AI בעזרת הספריה הרשמית
        client = genai.Client(api_key=API_KEY)

        # 3. שליחת השאלה לקבלת תשובה
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config={
                "system_instruction": (
                    "אתה עוזר שמספק תשובות **רק** בענייני אפייה. "
                    "אם השאלה אינה קשורה לאפייה, ענה בנימוס: "
                    "'מצטער, אני יכול לענות רק על שאלות אפייה.'"
                )
            },
        )

        return response.text

    except Exception as e:
        print(f"Gemini SDK Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"שגיאה בפנייה ל-Gemini: {e}"
        )