import os

import psycopg2
from psycopg2.extras import Json, RealDictCursor

# =========================
# Database Connection (Neon PostgreSQL)
# =========================
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("PGDATABASE_URL")
    or os.getenv("NEON_DATABASE_URL")
)

# postgresql://neondb_owner:npg_qRbIoM6zc5iw@ep-fragrant-rain-asv4gy1s-pooler.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"



def get_connection():
    """Create a new database connection when configuration is available."""
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not configured. Set DATABASE_URL (or PGDATABASE_URL/NEON_DATABASE_URL) before using the database layer."
        )
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
                   r.category_id, c.name AS category
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
                   r.category_id, c.name AS category
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
    """שליפת מתכונים לפי שם/מזהה קטגוריה"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        category_name = str(category_name).strip()
        if category_name.isdigit():
            query = """
                SELECT r.id, r.name, r.description, r.ingredients, r.instructions,
                       r.prep_time_minutes, r.servings, r.image_url, r.created_at,
                       r.category_id, c.name AS category
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.category_id = %s;
            """
            cursor.execute(query, (int(category_name),))
        else:
            query = """
                SELECT r.id, r.name, r.description, r.ingredients, r.instructions,
                       r.prep_time_minutes, r.servings, r.image_url, r.created_at,
                       r.category_id, c.name AS category
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
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


def add_recipe(name, description, ingredients, instructions, prep_time_minutes, servings, image_url, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO recipes (name, description, ingredients, instructions, prep_time_minutes, servings, image_url, category_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(
            query,
            (
                name,
                description,
                Json(ingredients) if isinstance(ingredients, (list, dict)) else ingredients,
                instructions,
                prep_time_minutes,
                servings,
                image_url,
                category_id,
            ),
        )
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
        allowed_fields = {
            "name",
            "description",
            "ingredients",
            "instructions",
            "prep_time_minutes",
            "servings",
            "image_url",
            "category_id",
        }
        fields = [field for field in updated_data if field in allowed_fields]
        if not fields:
            return False

        assignments = ", ".join(f"{field} = %s" for field in fields)
        values = [
            Json(updated_data[field])
            if field == "ingredients" and isinstance(updated_data[field], (list, dict))
            else updated_data[field]
            for field in fields
        ]
        values.append(recipe_id)
        cursor.execute(
            f"UPDATE recipes SET {assignments} WHERE id = %s;",
            values,
        )
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