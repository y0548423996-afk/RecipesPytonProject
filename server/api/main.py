from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.AIGemini import ask_gemini_baking
from models.Recipe import Recipe
from db.db import (
    get_all_recipes,
    get_recipe_by_id,
    get_recipes_by_category,
    add_recipe,
    update_recipe,
    delete_recipe
)
import traceback

app = FastAPI()

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def handle_exception(e: Exception):

    if isinstance(e, HTTPException):
        # אם זה כבר HTTPException, מחזירים אותו כמו שהוא
        raise e
    elif isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=str(e))
    elif isinstance(e, KeyError):
        raise HTTPException(status_code=404, detail=str(e))
    else:
        # כל שגיאה אחרת - 500 עם פירוט
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
            recipe.category
        )
        if not success:
            raise ValueError("קטגוריה לא קיימת")
        return {"message": "Recipe added successfully"}
    except Exception as e:
        handle_exception(e)

@app.put("/recipes/{recipe_id}")
def update_recipe_endpoint(recipe_id: int, recipe: Recipe):
    try:
        updated_data = recipe.model_dump()
        success = update_recipe(recipe_id, updated_data)
        if not success:
            raise KeyError(f"מתכון עם id {recipe_id} לא נמצא")
        return {"message": "המתכון עודכן בהצלחה"}
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

@app.post("/chat")
def ask(question: str = Body(..., embed=True)):
    try:
        return {
            "question": question,
            "answer": ask_gemini_baking(question)
        }
    except Exception as e:
        handle_exception(e)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
