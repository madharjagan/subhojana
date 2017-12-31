from Recipe import Recipe
from bs4 import BeautifulSoup as soup  
from urllib.request import urlopen as uReq

#For unit testing - Exposing it as REST service
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

class VegrecipesofindiaRecipe(Recipe):
	@app.route("/vegrecipesofindia/getRecipes")
	def getRecipes(self, page_uri):
		receipejson=[]
		rid = 1
		uClient = uReq(page_uri)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("article")
		for container in receipe_containers:
			rid = rid + 1;
			receipe_id = "vegrecipesofindia-recipe" + str(rid)
			receipejson.append({"rid": receipe_id ,"receipe_title": container.h2.a.string, "receipe_page_url": container.h2.a["href"], "receipe_page_image": container.div.a.img["src"],"receipe_page_description": container.div.p.text})
		uClient.close()
		return receipejson

	@app.route("/vegrecipesofindia/getIngredents")
	def getIngredents(self, page_url):
		print(page_url)
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
	
	@app.route("/vegrecipesofindia/getMethod")
	def getMethod(self, page_url):
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])