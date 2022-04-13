from flask import request, jsonify
import flask
import sys
import mysql.connector
import configparser

from flask_httpauth import HTTPBasicAuth

# initialization
auth = HTTPBasicAuth()
app = flask.Flask(__name__)
app.config["DEBUG"] = False

config=configparser.ConfigParser()
config.read('setting.ini')

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
    
    if conn.is_connected():
        print('Connected to MySQL database')
        # executing select query for recipes
        cursorRecipies.execute(f""" SELECT * FROM RECIPE WHERE RECIPE_NAME LIKE '%{recipeName}%'""")
        dataIngredients = cursorRecipies.fetchall ()
        result=[]
        if len(dataIngredients)>0:
            for row in dataIngredients:
                cursorRecipeIngredients.execute(f""" SELECT * FROM RECIPE_INGREDIENTS WHERE RECIPE_ID={row[0]}""")
                integrations=cursorRecipeIngredients.fetchall()
                listOfIngredientId=""
                count=0
                for integration in integrations:
                    if count==0:
                        listOfIngredientId=str(integration[2])
                    else:
                        listOfIngredientId=listOfIngredientId+","+str(integration[2])

                    count=count+1
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
                        'ingredients':listOfIngredients,
                        'totalTime':row[4],
                        'servings':row[5],
                        'cusine':row[6],
                        'course':row[7],
                        'diet':row[8],
                        'instructions':row[9]
                    }
                )
        
        if len(dataIngredients)>0:
            
            return jsonify(result)
        else:
            return jsonify({'message':"No Records Found"})
    else:
        print(" Not connected to database")
app.run(port=config.get('settings','port'))
