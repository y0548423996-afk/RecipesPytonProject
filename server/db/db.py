import psycopg2
from psycopg2.extras import RealDictCursor
import os

# =========================
# Database Connection (Neon PostgreSQL)
# =========================
DATABASE_URL = "postgresql://neondb_owner:npg_qRbIoM6zc5iw@ep-fragrant-rain-asv4gy1s-pooler.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    CONNECTION = psycopg2.connect(DATABASE_URL)
except psycopg2.Error as e:
    print("Database connection error:", e)
    raise


def get_connection():
    """יצירת חיבור חדש למסד הנתונים"""
    return psycopg2.connect(DATABASE_URL)


# =========================
# Database Operations
# =========================

def get_all_recipes():
    """שליפת כל המתכונים מהמסד כולל שם הקטגוריה מטבלת הקטגוריות"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT r.id, r.name, r.description, r.ingredients, r.instructions, 
                   r.prep_time_minutes, r.servings, r.image_url, r.created_at,
                   c.name AS category
            FROM recipes r
            LEFT JOIN categories c ON r.category_id = c.id;
        """
        cursor.execute(query)
        recipes = cursor.fetchall()
        return recipes
    except Exception as e:
        print("Error fetching all recipes:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def get_recipe_by_id(recipe_id):
    """שליפת מתכון ספציפי לפי מזהה כולל שם הקטגוריה"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT r.id, r.name, r.description, r.ingredients, r.instructions, 
                   r.prep_time_minutes, r.servings, r.image_url, r.created_at,
                   c.name AS category
            FROM recipes r
            LEFT JOIN categories c ON r.category_id = c.id
            WHERE r.id = %s;
        """
        cursor.execute(query, (recipe_id,))
        recipe = cursor.fetchone()
        return recipe
    except Exception as e:
        print(f"Error fetching recipe with id {recipe_id}:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def get_recipes_by_category(category_name):
    """שליפת מתכונים לפי שם הקטגוריה"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT r.id, r.name, r.description, r.ingredients, r.instructions, 
                   r.prep_time_minutes, r.servings, r.image_url, r.created_at,
                   c.name AS category
            FROM recipes r
            INNER JOIN categories c ON r.category_id = c.id
            WHERE c.name = %s;
        """
        cursor.execute(query, (category_name,))
        recipes = cursor.fetchall()
        return recipes
    except Exception as e:
        print(f"Error fetching recipes by category {category_name}:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def add_recipe(name, description, ingredients, instructions, prep_time_minutes, servings, image_url, category):
    """הוספת מתכון חדש"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO recipes (name, description, ingredients, instructions, prep_time_minutes, servings, image_url, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (name, description, ingredients, instructions, prep_time_minutes, servings, image_url, category))
        conn.commit()
        return True
    except Exception as e:
        print("Error adding recipe:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def update_recipe(recipe_id, updated_data):
    """עדכון מתכון קיים לפי מזהה"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE recipes
            SET name = %s, description = %s, ingredients = %s, instructions = %s,
                prep_time_minutes = %s, servings = %s, image_url = %s, category_id = %s
            WHERE id = %s;
        """
        cursor.execute(query, (
            updated_data.get('name'),
            updated_data.get('description'),
            updated_data.get('ingredients'),
            updated_data.get('instructions'),
            updated_data.get('prep_time_minutes'),
            updated_data.get('servings'),
            updated_data.get('image_url'),
            updated_data.get('category_id'),
            recipe_id
        ))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating recipe {recipe_id}:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def delete_recipe(recipe_id):
    """מחיקת מתכון לפי מזהה"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM recipes WHERE id = %s;", (recipe_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting recipe {recipe_id}:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()