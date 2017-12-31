from Recipe import Recipe

class RecipeDetails(Recipe):
	def __init__(self, state):
		self.state = state

	def set_state(self, state):
		self.state = state

	def getRecipes(self, page_uri):
		return self.state.getRecipes(page_uri)
		
	def getIngredents(self, page_url):
		return self.state.getIngredents(page_url)

	def getMethod(self, page_url):
		return self.state.getMethod(page_url)