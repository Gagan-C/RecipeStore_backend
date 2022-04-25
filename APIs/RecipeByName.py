from flask import request, jsonify
import flask
import sys
import mysql.connector
import configparser
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

# initialization
auth = HTTPBasicAuth()
app = flask.Flask(__name__)
app.config["DEBUG"] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
config=configparser.ConfigParser()
config.read('setting.ini')

def ConvertListToCommaSeperatedString(p,index):
    stringval=""
    count=0;
    for i in p:
        if (count==0):
            stringval=str(i[index])
        else:
            stringval=stringval+","+str(i[index])
        count=count+1
    return stringval
def generateDictonaryWithInputs(recipes, recipeIngredients, ingredients):
    result=[]
    for recipe in recipes:
        listOfingredientsIds=[]
        for recipeIngredient in recipeIngredients:
            if(recipeIngredient[1]==recipe[0]):
                listOfingredientsIds.append(recipeIngredient[2])
        listOfIngredients=[]
        for ingredientid in listOfingredientsIds:
            for ingredient in ingredients:
                if(ingredientid == ingredient[0]):
                    listOfIngredients.append(
                        {
                            'ingredientId':ingredient[0],
                            'ingredientName':ingredient[1]
                        }
            )
        result.append(
                {
                        'recipeId':recipe[0],
                        'recipeName':recipe[1],
                        'listOfIngredientIds':listOfingredientsIds,
                        'prepTime':recipe[2],
                        'cookTime':recipe[3],
                        'ingredients':listOfIngredients,
                        'totalTime':recipe[4],
                        'servings':recipe[5],
                        'cusine':recipe[6],
                        'course':recipe[7],
                        'diet':recipe[8],
                        'instructions':recipe[9]
                    }
            )
    return result

@auth.verify_password
def verify_password(username, password):
    if username in ['admin'] and password in ['Admin123']:
        return True
    else:
        return False

@app.route('/api/recipe/byName/', methods=['GET'])
@auth.login_required
def RecipeByName():
    
    conn = mysql.connector.MySQLConnection(host=config.get('rs_db','host'),
                                       port=config.get('rs_db','port'),
                                       database=config.get('rs_db','database'),
                                       user=config.get('rs_db','user'),
                                       password=config.get('rs_db','password'))
    cursorIngredients = conn.cursor()
    cursorRecipies=conn.cursor()
    cursorRecipeIngredients=conn.cursor()
    if 'recipeName' in request.args:
        recipeName = str(request.args['recipeName'])
    else:
        return jsonify({'message':"Wrong parameters"})
    if conn.is_connected():
        print('Connected to MySQL database')
        # executing select query for recipes
        cursorRecipies.execute(f""" SELECT * FROM RECIPE WHERE RECIPE_NAME LIKE '%{recipeName}%'""")
        dataIngredients = cursorRecipies.fetchall()
        result=[]
        if len(dataIngredients)>0:
            for row in dataIngredients:
                cursorRecipeIngredients.execute(f""" SELECT * FROM RECIPE_INGREDIENTS WHERE RECIPE_ID={row[0]}""")
                integrations=cursorRecipeIngredients.fetchall()
                listOfIngredientId=ConvertListToCommaSeperatedString(integrations,2)
                cursorIngredients.execute(f"""SELECT * FROM INGREDIENT WHERE INGREDIENT_ID IN ({listOfIngredientId})""")
                ingredients=cursorIngredients.fetchall()
                listOfIngredients=[]
                for ingredient in ingredients:
                    listOfIngredients.append(
                        {
                            'ingredientId':ingredient[0],
                            'ingredientName':ingredient[1]
                        }
                    )
                result.append(
                    {
                        'recipeId':row[0],
                        'recipeName':row[1],
                        'prepTime':row[2],
                        'cookTime':row[3],
                        'totalTime':row[4],
                        'servings':row[5],
                        'cusine':row[6],
                        'course':row[7],
                        'diet':row[8],
                        'instructions':row[9],
                        'ingredients':listOfIngredients
                    }
                )
        
        if len(dataIngredients)>0:
            
            return jsonify(result)
        else:
            return jsonify({'message':"No Records Found"})
    else:
        print("Not connected to database")

@app.route('/api/recipe/byIngredients/', methods=['GET'])
@auth.login_required
def RecipeByIngredients():
    conn = mysql.connector.MySQLConnection(host=config.get('rs_db','host'),
                                       port=config.get('rs_db','port'),
                                       database=config.get('rs_db','database'),
                                       user=config.get('rs_db','user'),
                                       password=config.get('rs_db','password'))
    cursorIngredients = conn.cursor()
    cursorRecipes=conn.cursor()
    cursorRecipeIngredients=conn.cursor()
    cursorRecipeIngredients2=conn.cursor()
    cursorIngredients2=conn.cursor()
    if 'ingredients' in request.args:
        ingredientsInput = request.args['ingredients']
        
    else:
        return jsonify({'message':"Wrong parameters"})
    if conn.is_connected():
        print('Connected to MySQL database')
    else:
        return jsonify({'message':"Not connected to database"})
    
    cursorIngredients.execute(f"""SELECT * FROM INGREDIENT WHERE INGREDIENT_NAME REGEXP '{ingredientsInput}'""")
    
    ingredients=cursorIngredients.fetchall()
    listOfIngredientIds=ConvertListToCommaSeperatedString(ingredients,0)
    

    cursorRecipeIngredients.execute(f"""SELECT * FROM RECIPE_INGREDIENTS WHERE INGREDIENT_ID IN ({listOfIngredientIds})""")
    recipeIngredients=cursorRecipeIngredients.fetchall()
    listOfRecipeIds=ConvertListToCommaSeperatedString(recipeIngredients,1)
    
    cursorRecipeIngredients2.execute(f"""SELECT * FROM RECIPE_INGREDIENTS WHERE RECIPE_ID IN ({listOfRecipeIds})""")
    recipeIngredients2=cursorRecipeIngredients2.fetchall()
    listOfIngredientIds2=ConvertListToCommaSeperatedString(recipeIngredients2,2)
    cursorIngredients2.execute(f"""SELECT * FROM INGREDIENT WHERE INGREDIENT_ID IN ({listOfIngredientIds2})""")
    ingredients2=cursorIngredients2.fetchall()
    cursorRecipes.execute(f"""SELECT * FROM RECIPE WHERE RECIPE_ID IN ({listOfRecipeIds})""")
    recipes=cursorRecipes.fetchall()
    return jsonify(generateDictonaryWithInputs(recipes,recipeIngredients2, ingredients2))

@app.route('/api/recipe/potentialRecipe/', methods=['POST'])
@auth.login_required
def AddPotentialRecipe():
    conn = mysql.connector.MySQLConnection(host=config.get('rs_db','host'),
                                       port=config.get('rs_db','port'),
                                       database=config.get('rs_db','database'),
                                       user=config.get('rs_db','user'),
                                       password=config.get('rs_db','password'))
    cursorPotential = conn.cursor()
    cursorPotential.execute(f"""INSERT INTO RECIPE_PROPOSAL (RECIPE_NAME,PREP_TIME,COOK_TIME,TOTAL_TIME,SERVINGS,CUISINE,COURSE,DIET,INSTRUCTIONS,INGREDIENTS) VALUES ('{request.args['RecipeName']}',{request.args['PrepTime']},{request.args['CookTime']},{request.args['TotalTime']},{request.args['Servings']},'{request.args['Cuisine']}','{request.args['Course']}','{request.args['Diet']}','{request.args['Instructions']}','{request.args['Ingredients']}')""")
    
    conn.commit()
    cursorPotential.close()
    return jsonify({'status':"success"})
app.run(port=config.get('settings','port'))
