from Recipe import Recipe
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

class VahrehvahRecipe(Recipe):
	def getRecipes(self, page_uri):
		receipejson=[]
		rid = 1
		uClient = uReq(page_uri)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "col-md-12 border_reciipe"})
		for container in receipe_containers:
			rid = rid + 1;
			receipe_id = "vahrehvah-recipe" + str(rid)
			receipe = container.div.findAll("div")
			receipejson.append({"id": receipe_id ,"receipe_title": receipe[0].h2.a["title"], "receipe_page_url": receipe[0].h2.a["href"], "receipe_page_image": receipe[1].img["src"],"receipe_page_description": receipe[2].p.text})
		uClient.close()
		return receipejson

	def getIngredents(self, page_url):
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])
		
	def getMethod(self, page_url):
		uClient = uReq(page_url)
		page_soup = soup(uClient.read(), "html.parser")
		receipe_containers = page_soup.findAll("div", {"class": "wprm-recipe-ingredients-container"})
		return str(receipe_containers[0])