from pydantic import BaseModel
from typing import List, Optional


class Recipe(BaseModel):
   name: str
   description: Optional[str] = ""
   ingredients: List[str]
   instructions: str
   prep_time_minutes: int
   servings: int
   image_url: Optional[str] = None
   category_id: int  # שינוי מ-category: str ל-category_id: int

