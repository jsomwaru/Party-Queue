import urllib.parse 
class SongReq():
	def __init__ (self, artist, song):
		self.artist = artist 
		self.song = song
		self.url = None 
	
	def formatUrl (self):
		enArtist = urllib.parse.quote(self.artist)
		ensong  = urllib.parse.quote(self.song)
		self.url = 'http://localhost:9999/get_by_search?type=song&artist={0}&song={1}'.format(enArtist, ensong)
		print(self.url)

