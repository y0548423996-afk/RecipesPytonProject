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
    category_id: int  # שימי לב: category_id כמספר!
