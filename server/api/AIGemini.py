# file: api_gemini.py
import os
import requests
import urllib3
from fastapi import HTTPException

# מבטל אזהרות SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = os.environ.get("API_KEY")


def ask_gemini_baking(question: str) -> str:
    # 1. בדיקה שהמפתח קיים בסביבת העבודה
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY is missing in environment variables",
        )

    # 2. שימוש במודל נתמך ובניית ה-URL
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"role": "user", "parts": [{"text": question}]}],
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "אתה עוזר שמספק תשובות **רק** בענייני אפייה. "
                        "אם השאלה אינה קשורה לאפייה, ענה בנימוס: "
                        "'מצטער, אני יכול לענות רק על שאלות אפייה.'"
                    )
                }
            ]
        },
    }

    try:
        response = requests.post(
            gemini_url,
            json=payload,
            verify=False,
            timeout=30,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"שגיאת חיבור ל-Gemini: {e}"
        )

    # 3. הדפסת הודעת השגיאה המלאה ל-Logs ב-Render אם יש תקלה
    if response.status_code != 200:
        print(f"Gemini API Error Status: {response.status_code}")
        print(f"Gemini API Error Response: {response.text}")
        raise HTTPException(
            status_code=500, detail=f"שגיאה מ-Gemini: {response.text}"
        )

    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500, detail="שגיאה בקריאת הנתונים מה-API"
        )