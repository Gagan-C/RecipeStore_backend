# RecipeStore_backend

## Steps to run backend server

* Install Python and pip tool
* Install or use external MySQL server
* Run commands in Prerequisites/prerequisites.txt script
* Run scripts from Database/scripts folder to create tables and database. Make sure there are no naming conflicts for database name before executing script
* Import data into tables using mysql workbench or CLI. data is located in Database folder with appropirate table names. Import sequence as follows:  
  * Ingredients
  * Recipes
  * Recipe Ingredients
* Change API's/Setting.ini if you have a different server or plan to run service on a different port
* Run RecipeByName.py to start server

## Sources
* Data used in the project is downloaded from https://www.kaggle.com/kanishk307/6000-indian-food-recipes-dataset 
* Front end of the application is avaiable at: https://github.com/Gowtham369/Recipe_Store
