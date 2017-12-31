from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import json

import threading

from flask import Flask
from flask import request
from flask_cors import CORS

from VegrecipesofindiaRecipe import VegrecipesofindiaRecipe
from VahrehvahRecipe import VahrehvahRecipe
from YoutubeRecipe import YoutubeRecipe
from SailusfoodRecipe import SailusfoodRecipe
from ThasneenRecipe import ThasneenRecipe
from RecipeDetails import RecipeDetails

app = Flask(__name__)
CORS(app)

receipe_id=1
receipejson=[]

@app.route("/subhojana")
def subhojana():
	global receipejson
	receipejson = []
	sitelist = ["http://www.youtube.com/results?search_query=", 
				"http://www.vegrecipesofindia.com/?s=",
				"http://www.vahrehvah.com/searchrecipe?recipe_name=",
				"http://www.sailusfood.com/search/?q=",
				"http://www.thasneen.com/cooking/?s="
			   ]
	searchstring = request.args.get('searchstring')
	threads = []
	for site in sitelist:
		thread = threading.Thread(target=getRecipes, args=(site,searchstring))
		thread.start()
		threads.append(thread)
	for thread in threads:
		thread.join()
	return json.dumps(receipejson)

def whichWebsite(page_url):
	if "vegrecipesofindia" in page_url:
		recipe = VegrecipesofindiaRecipe()
	elif "vahrehvah" in page_url:
		recipe = VahrehvahRecipe()
	elif "youtube" in page_url:
		recipe = YoutubeRecipe()
	elif "sailusfood" in page_url:
		recipe = SailusfoodRecipe()
	elif "thasneen" in page_url:
		recipe = ThasneenRecipe()
	else:
		recipe = VegrecipesofindiaRecipe()
	return recipe

@app.route("/getIngredient")
def getIngredient():
	page_url = request.args.get('page_url')
	recipeDetails = RecipeDetails(whichWebsite(page_url))
	return recipeDetails.getIngredents(page_url)

@app.route("/getMethod")
def getMethod():
	page_url = request.args.get('page_url')
	recipeDetails = RecipeDetails(VegrecipesofindiaRecipe())
	return recipeDetails.getMethod(page_url)

@app.route("/vegrecipesofindia")
def getRecipes(page_url, searchstring):
	global receipejson
	page_uri = page_url + searchstring
	print(page_uri)
	recipeDetails = RecipeDetails(whichWebsite(page_url))
	receipejson += recipeDetails.getRecipes(page_uri)
