import re

class formatter:

	def __init__ (self, artist, title):
		self.artist = artist
		self.title = title
		## Starts with shell url will be properly formatted to provide to proxy
		self.url = 'http://localhost:9999/get_by_search?type=song&artist=XXXX&title=XXXX'
	
	def check_input (artist, title):
		if(artist.len() > 60 and title.len() > 60):
			return False
		else:
			return True
	
	def format_url (self):
		re.sub(r' ', '%20' , self.url)
		