from Recipe import Recipe
from bs4 import BeautifulSoup as soup  
from urllib.request import urlopen as uReq
import requests

#For unit testing - Exposing it as REST service
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

class YoutubeRecipe(Recipe):
	@app.route("/youtube/getRecipes")
	def getRecipes(self, page_uri):
		receipejson=[]
		rid = 1
		#uClient = uReq(page_uri, headers={'User-Agent': 'Mozilla/5.0'})
		page_soup = soup(requests.get(page_uri, {'User-Agent': 'Mozilla/5.0'}).text, "html.parser")
		receipe_containers = page_soup.findAll("div" , {"class": "yt-lockup-dismissable yt-uix-tile"})
		for container in receipe_containers:
			rid = rid + 1;
			receipe_id = "youtube-recipe" + str(rid)
			images = container.findAll("img")
			title = container.findAll("a", {"class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link "})
			url = "https://www.youtube.com/"+title[0]["href"]
			desc = container.findAll("div", {"class": "yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"})
			receipejson.append({"id": receipe_id ,"receipe_title": title[0].text ,"receipe_page_url": url, "receipe_page_image": images[0]["src"],"receipe_page_description": title[0].text})
		#uClient.close()
		return receipejson

	@app.route("/youtube/getIngredents")
	def getIngredents(self, page_url):
		print(page_url)
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
	
	@app.route("/youtube/getMethod")
	def getMethod(self, page_url):
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
	
	@app.route("/youtube")
	def youtube(searchstring):
		global receipe_id
		global receipejson
		page_url = "http://www.youtube.com/results?search_query="+searchstring
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div" , {"class": "yt-lockup-dismissable yt-uix-tile"})
		for container in receipe_containers:
			receipe_id = receipe_id + 1
			images = container.findAll("img")
			title = container.findAll("a", {"class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link "})
			url = "http://www.youtube.com/"+title[0]["href"]
			desc = container.findAll("div", {"class": "yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"})
			receipejson.append({"id": receipe_id ,"receipe_title": title[0].text ,"receipe_page_url": url, "receipe_page_image": "https://www.youtube.com/"+images[0]["src"],"receipe_page_description": title[0].text})

		uClient.close()