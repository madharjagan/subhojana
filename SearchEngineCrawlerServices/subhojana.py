from flask import Flask
from flask import request
from flask_cors import CORS
import threading
import json
from VegrecipesofindiaRecipe import VegrecipesofindiaRecipe
from VahrehvahRecipe import VahrehvahRecipe
from RecipeDetails import RecipeDetails
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
app = Flask(__name__)
CORS(app)

receipe_id=1
receipejson=[]

@app.route("/subhojana")
def subhojana():
	global receipejson
	receipejson = []
	sitelist = ["http://www.vegrecipesofindia.com/?s=","http://www.vahrehvah.com/searchrecipe?recipe_name="]
	searchstring = request.args.get('searchstring')
	threads = []
	for site in sitelist:
		thread = threading.Thread(target=getRecipes, args=(site,searchstring))
		thread.start()
		threads.append(thread)
	for thread in threads:
		thread.join()
		
	#receipejson = receipejson + getRecipes("http://www.vegrecipesofindia.com/?s=", searchstring)
	#receipejson = receipejson + getRecipes("https://www.vahrehvah.com/searchrecipe?recipe_name=", searchstring)
	#vegrecipesofindia(searchstring)
	#vahrehvah(searchstring)
	#thasneen(searchstring)
	#sailusfood(searchstring)
	#youtube(searchstring)
	return json.dumps(receipejson)

def whichWebsite(page_url):
	if "vegrecipesofindia" in page_url:
		recipe = VegrecipesofindiaRecipe()
	elif "vahrehvah" in page_url:
		recipe = VahrehvahRecipe()
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
	
@app.route("/vahrehvah")
def vahrehvah(searchstring):
	global receipe_id
	global receipejson
	page_url = "http://www.vahrehvah.com/searchrecipe?recipe_name="+searchstring
	uClient = uReq(page_url)
	page_soup = soup(uClient.read(), "html.parser")
	receipe_containers = page_soup.findAll("div", {"class": "col-md-12 border_reciipe"})

	for container in receipe_containers:
		receipe = container.div.findAll("div")
		receipe_id = receipe_id + 1;
		receipejson.append({"id": receipe_id ,"receipe_title": receipe[0].h2.a["title"], "receipe_page_url": receipe[0].h2.a["href"], "receipe_page_image": receipe[1].img["src"],"receipe_page_description": receipe[2].p.text})

	uClient.close()

@app.route("/thasneen")
def thasneen(searchstring):
	global receipe_id
	global receipejson
	page_url = "http://www.thasneen.com/cooking/?s="+searchstring
	uClient = uReq(page_url)
	page_soup = soup(uClient.read(), "html.parser")
	receipe_containers = page_soup.findAll("div", {"class": "homepost small-image-left"})
	for container in receipe_containers:
		receipe_heading = container.findAll("div",{"class": "homepost-heading"})
		receipe_image = container.findAll("div",{"class": "content-image"})
		receipe_description = container.findAll("div",{"class": "content-area"})
		receipe_id = receipe_id + 1
		receipejson.append({"id": receipe_id ,"receipe_title": receipe_heading[0].h2.text, "receipe_page_url": receipe_heading[0].h2.a["href"], "receipe_page_image": receipe_image[0].a.img["data-lazy-src"],"receipe_page_description": receipe_description[0].p.text})

	uClient.close()
	
@app.route("/sailusfood")
def sailusfood(searchstring):
	global receipe_id
	global receipejson
	page_url = "http://www.sailusfood.com/search/?q="+searchstring
	uClient = uReq(page_url)
	page_soup = soup(uClient.read(), "html.parser")
	receipe_containers = page_soup.findAll("div", {"class": "col-lg-12 col-md-12"})
	for container in receipe_containers:
		receipe_id = receipe_id + 1
		receipe_a = container.findAll("div", {"class": "row"})
		receipejson.append({"id": receipe_id ,"receipe_title": receipe_a[0].a.img["alt"] ,"receipe_page_url": receipe_a[0].a["href"], "receipe_page_image": receipe_a[0].a.img["src"],"receipe_page_description": receipe_a[0].a.img["alt"]})

	uClient.close()
	

@app.route("/youtube")
def youtube(searchstring):
	global receipe_id
	global receipejson
	page_url = "https://www.youtube.com/results?search_query="+searchstring
	uClient = uReq(page_url)
	page_soup = soup(uClient.read(), "html.parser")
	receipe_containers = page_soup.findAll("div" , {"class": "yt-lockup-dismissable yt-uix-tile"})
	for container in receipe_containers:
		receipe_id = receipe_id + 1
		images = container.findAll("img")
		title = container.findAll("a", {"class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link "})
		url = "https://www.youtube.com/"+title[0]["href"]
		desc = container.findAll("div", {"class": "yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"})
		receipejson.append({"id": receipe_id ,"receipe_title": title[0].text ,"receipe_page_url": url, "receipe_page_image": images[0]["src"],"receipe_page_description": title[0].text})

	uClient.close()

