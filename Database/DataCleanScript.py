import csv
import time
from googletrans import Translator, constants
from pprint import pprint

def unique(list1):
 
    # initialize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
translator=Translator()
f=open("IndianFoodDataSetCSV.csv","r",encoding="utf_8_sig")
ingredientsFile=open("Ingredients.csv","w",encoding="utf_8_sig")
recipeFile=open("Recipe.csv","w",encoding="utf_8_sig")
recipeIngredientsFile=open("RecipeIngredients.csv","w",encoding="utf_8_sig")
reader = csv.reader(f)
#ingredientsCount=1
recipeCount=1
recipeIngredientCount=1

ingredients=[]
begin=time.time()
for recipe in reader:
    
    
    #flat_list = [item for sublist in recipe[4].split(',') for item in sublist]
    for ingredient in recipe[4].split(','):
        try:
            ingredients.index(ingredient)
        except ValueError:
            ingredients.append(ingredient)
            ingredientsFile.write(str(ingredients.index(ingredient))+","+str(ingredient)+"\n")
            
        recipeIngredientsFile.write(str(recipeIngredientCount)+","+str(recipeCount)+","+str(ingredients.index(ingredient))+"\n")
        
        recipeIngredientCount=recipeIngredientCount+1
        #ingredientsCount=ingredientsCount+1

    translation=translator.translate(recipe[1])   
    translation2=translator.translate(recipe[12]) 
    recipeFile.write(str(recipeCount)+","+translation.text.replace(","," ")+","+recipe[5]+","+recipe[6]+ ","+recipe[7]+","+recipe[8]+","+recipe[9]+","+recipe[10]+","+recipe[11]+","+translation2.text.replace(","," ")+"\n")
    recipeCount=recipeCount+1


#flat_list = [item for sublist in ingredients for item in sublist]
#uniqueIngredients=unique(flat_list)
#for i in uniqueIngredients:
 #   ingredents.write(str(ingredientsCount)+","+i+"\n")
  #  ingredientsCount=ingredientsCount+1

end=time.time()
print(f"Total runtime of the program is {end - begin}")

f.close()
ingredientsFile.close()
recipeFile.close()
recipeIngredientsFile.close()
