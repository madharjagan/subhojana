import abc

class Recipe(metaclass=abc.ABCMeta):
    
	@abc.abstractmethod
	def getRecipes(self, page_uri):
		pass
		
	@abc.abstractmethod
	def getIngredents(self, page_url):
		pass

	@abc.abstractmethod
	def getMethod(self, page_url):
		pass