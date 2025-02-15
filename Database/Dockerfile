FROM mysql:latest


COPY ./scripts/Recipe_Store_DDL.sql /docker-entrypoint-initdb.d/1.sql

# Ingredients
COPY ./Ingredients.csv /var/lib/mysql-files/Ingredients.csv
COPY ./scripts/load_ingredients.sql /docker-entrypoint-initdb.d/2.sql

# Recipes
COPY ./Recipe.csv /var/lib/mysql-files/Recipe.csv
COPY ./scripts/load_recipes.sql /docker-entrypoint-initdb.d/3.sql

# RecipeIngredients
COPY ./RecipeIngredients.csv /var/lib/mysql-files/RecipeIngredients.csv
COPY ./scripts/load_recipe_ingredients.sql /docker-entrypoint-initdb.d/4.sql

# Export the port
EXPOSE 3306
 

