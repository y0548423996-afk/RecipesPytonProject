from pydantic import BaseModel
from typing import List, Optional


class Recipe(BaseModel):
   name: str
   description: Optional[str] = ""
   ingredients: List[str]  # חשוב: List עם L גדולה מיובא מ-typing
   instructions: str
   prep_time_minutes: int
   servings: int
   image_url: Optional[str] = None
   category: str

