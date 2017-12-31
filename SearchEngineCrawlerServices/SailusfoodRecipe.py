from Recipe import Recipe
from bs4 import BeautifulSoup as soup  
from urllib.request import urlopen as uReq

#For unit testing - Exposing it as REST service
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

class SailusfoodRecipe(Recipe):
	@app.route("/sailusfood/getRecipes")
	def getRecipes(self, page_uri):
		receipejson=[]
		rid = 1
		uClient = uReq(page_uri)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "col-lg-12 col-md-12"})
		for container in receipe_containers:
			rid = rid + 1;
			receipe_id = "sailusfood-recipe" + str(rid)
			receipe_a = container.findAll("div", {"class": "row"})
			receipejson.append({"id": receipe_id ,"receipe_title": receipe_a[0].a.img["alt"] ,"receipe_page_url": receipe_a[0].a["href"], "receipe_page_image": receipe_a[0].a.img["src"],"receipe_page_description": receipe_a[0].a.img["alt"]})
		uClient.close()
		return receipejson

	@app.route("/sailusfood/getIngredents")
	def getIngredents(self, page_url):
		print(page_url)
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
	
	@app.route("/sailusfood/getMethod")
	def getMethod(self, page_url):
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
		
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