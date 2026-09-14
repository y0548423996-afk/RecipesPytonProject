import sys
import traceback
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.AIGemini import ask_gemini_baking
from db.db import (
    add_recipe,
    delete_recipe,
    get_all_recipes,
    get_recipe_by_id,
    get_recipes_by_category,
    update_recipe,
)
from models.Recipe import Recipe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecipeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    ingredients: list[str] | None = None
    instructions: str | None = None
    prep_time_minutes: int | None = None
    servings: int | None = None
    image_url: str | None = None
    category_id: int | None = None


def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        raise e
    if isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=str(e))
    if isinstance(e, KeyError):
        raise HTTPException(status_code=404, detail=str(e))
    detail = f"{str(e)}\n{traceback.format_exc()}"
    raise HTTPException(status_code=500, detail=detail)


@app.get("/recipes")
def get_recipes():
    try:
        return get_all_recipes()
    except Exception as e:
        handle_exception(e)


@app.get("/recipes/{id}")
def get_recipe(id: int):
    try:
        recipe = get_recipe_by_id(id)
        if not recipe:
            raise KeyError(f"מתכון עם id {id} לא נמצא")
        return recipe
    except Exception as e:
        handle_exception(e)


@app.get("/recipes/category/{category_name}")
def get_recipe_category(category_name: str):
    try:
        recipes = get_recipes_by_category(category_name)
        if recipes is None or len(recipes) == 0:
            raise KeyError(f"לא נמצאו מתכונים בקטגוריה {category_name}")
        return recipes
    except Exception as e:
        handle_exception(e)


@app.post("/recipes")
def create_recipe(recipe: Recipe):
    try:
        success = add_recipe(
            recipe.name,
            recipe.description,
            recipe.ingredients,
            recipe.instructions,
            recipe.prep_time_minutes,
            recipe.servings,
            recipe.image_url,
            recipe.category_id,
        )
        if not success:
            raise ValueError("שגיאה בהוספת המתכון")
        return {"message": "Recipe added successfully"}
    except Exception as e:
        handle_exception(e)


@app.put("/recipes/{recipe_id}")
def update_recipe_endpoint(recipe_id: int, updated_data: dict = Body(...)):
    try:
        if not updated_data:
            raise ValueError("לא נשלחו שדות לעדכון")
        payload = {key: value for key, value in updated_data.items() if value is not None}
        if not payload:
            raise ValueError("לא נשלחו שדות לעדכון")
        success = update_recipe(recipe_id, payload)
        if not success:
            raise KeyError(f"מתכון עם id {recipe_id} לא נמצא")
        return {"message": "Recipe updated successfully"}
    except Exception as e:
        handle_exception(e)


@app.post("/chat")
def chat_endpoint(payload: dict = Body(...)):
    try:
        question = payload.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="שאלה חסרה")
        answer = ask_gemini_baking(question)
        return {"answer": answer}
    except Exception as e:
        handle_exception(e)


@app.delete("/recipes/{recipe_id}")
def delete_recipe_api(recipe_id: int):
    try:
        success = delete_recipe(recipe_id)
        if not success:
            raise KeyError(f"מתכון עם id {recipe_id} לא נמצא")
        return {"message": "המוצר נמחק בהצלחה"}
    except Exception as e:
        handle_exception(e)


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
