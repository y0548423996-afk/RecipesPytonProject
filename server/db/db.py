import pyodbc


# =========================
# Database Connection (once)
# =========================
try:
  CONNECTION = pyodbc.connect(
      "DRIVER={ODBC Driver 17 for SQL Server};"
      "SERVER=localhost\\SQLEXPRESS;"
      "DATABASE=Recipes;"
      "Trusted_Connection=yes;"
  )
except pyodbc.Error as e:
  print("Database connection error:", e)
  raise








# =========================
# Helpers
# =========================
def rows_to_dict(cursor):
  columns = [column[0] for column in cursor.description]
  return [dict(zip(columns, row)) for row in cursor.fetchall()]








# =========================
# Queries
# =========================
def get_all_recipes():
  try:
      cursor = CONNECTION.cursor()
      cursor.execute(
          "SELECT id, name, description, image_url FROM recipes"
      )
      result = rows_to_dict(cursor)
      cursor.close()
      return result
  except pyodbc.Error as e:
      print("DB error:", e)
      raise








def get_recipe_by_id(recipe_id: int):
  try:
      cursor = CONNECTION.cursor()
      cursor.execute(
          "SELECT * FROM recipes WHERE id = ?",
          (recipe_id,)
      )
      row = cursor.fetchone()
      if not row:
          cursor.close()
          return None




      columns = [column[0] for column in cursor.description]
      result = dict(zip(columns, row))
      cursor.close()
      return result
  except pyodbc.Error as e:
      print("DB error:", e)
      raise








def get_recipes_by_category(category_name: str):
  try:
      cursor = CONNECTION.cursor()
      cursor.execute("""
          SELECT r.*
          FROM recipes r
          JOIN categories c ON r.category_id = c.id
          WHERE c.name = ?
      """, (category_name,))
      result = rows_to_dict(cursor)
      cursor.close()
      return result
  except pyodbc.Error as e:
      print("DB error:", e)
      raise








def add_recipe(
  name,
  description,
  ingredients,
  instructions,
  prep_time_minutes,
  servings,
  image_url,
  category_name
):
  try:
      cursor = CONNECTION.cursor()




      cursor.execute(
          "SELECT id FROM categories WHERE name = ?",
          (category_name,)
      )
      row = cursor.fetchone()
      if not row:
          cursor.close()
          return False




      category_id = row[0]




      cursor.execute("""
          INSERT INTO recipes
          (name, description, ingredients, instructions,
           prep_time_minutes, servings, image_url, category_id)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """, (
          name,
          description,
          ", ".join(ingredients) if isinstance(ingredients, list) else ingredients,
          instructions,
          prep_time_minutes,
          servings,
          image_url,
          category_id
      ))




      CONNECTION.commit()
      cursor.close()
      return True
  except pyodbc.Error as e:
      print("DB error:", e)
      raise








def update_recipe(recipe_id: int, updated_recipe: dict):
  try:
      cursor = CONNECTION.cursor()




      ingredients_str = (
          ", ".join(updated_recipe["ingredients"])
          if isinstance(updated_recipe["ingredients"], list)
          else updated_recipe["ingredients"]
      )




      cursor.execute("""
          UPDATE recipes
          SET name = ?,
              description = ?,
              ingredients = ?,
              instructions = ?,
              prep_time_minutes = ?,
              servings = ?,
              image_url = ?
          WHERE id = ?
      """, (
          updated_recipe["name"],
          updated_recipe["description"],
          ingredients_str,
          updated_recipe["instructions"],
          updated_recipe["prep_time_minutes"],
          updated_recipe["servings"],
          updated_recipe["image_url"],
          recipe_id
      ))




      CONNECTION.commit()
      updated = cursor.rowcount > 0
      cursor.close()
      return updated
  except pyodbc.Error as e:
      print("DB error:", e)
      raise








def delete_recipe(recipe_id: int):
  try:
      cursor = CONNECTION.cursor()
      cursor.execute(
          "DELETE FROM recipes WHERE id = ?",
          (recipe_id,)
      )
      CONNECTION.commit()
      deleted = cursor.rowcount > 0
      cursor.close()
      return deleted
  except pyodbc.Error as e:
      print("DB error:", e)
      raise








# =========================
# Close connection on exit
# =========================
# CONNECTION.close()




