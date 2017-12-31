from Recipe import Recipe
from bs4 import BeautifulSoup as soup  
from urllib.request import urlopen as uReq

#For unit testing - Exposing it as REST service
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

class ThasneenRecipe(Recipe):
	@app.route("/thasneen/getRecipes")
	def getRecipes(self, page_uri):
		receipejson=[]
		rid = 1
		uClient = uReq(page_uri)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "homepost small-image-left"})
		for container in receipe_containers:
			rid = rid + 1;
			receipe_id = "thasneen-recipe" + str(rid)
			receipe_heading = container.findAll("div",{"class": "homepost-heading"})
			receipe_image = container.findAll("div",{"class": "content-image"})
			receipe_description = container.findAll("div",{"class": "content-area"})
			receipejson.append({"id": receipe_id ,"receipe_title": receipe_heading[0].h2.text, "receipe_page_url": receipe_heading[0].h2.a["href"], "receipe_page_image": receipe_image[0].a.img["data-lazy-src"],"receipe_page_description": receipe_description[0].p.text})
		uClient.close()
		return receipejson

	@app.route("/thasneen/getIngredents")
	def getIngredents(self, page_url):
		print(page_url)
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
	
	@app.route("/thasneen/getMethod")
	def getMethod(self, page_url):
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
	
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