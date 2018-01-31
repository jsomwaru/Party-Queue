import vlc 
import requests
from time import sleep

class Sounds:
	
	def run (self, url):
		self.list_player = vlc.MediaListPlayer()
		self.list = vlc.MediaList(url)
		self.list_player.set_media_list(self.list)
		self.list_player.play()
		
		while True:
			if self.list_player.is_playing():
				continue
			elif self.list_player.is_playing() == -1 and self.list.count() != 0:
				continue
			elif self.list_player.is_playing() == -1 and self.list.count() == 0:
				self.instance.release()
				break
		

if __name__ == '__main__':
	
	urls = [ 
			'http://localhost:9999/get_by_search?type=song&artist=king%20krule&title=biscuit%20town'
	]
	
	sound = Sounds()
	sound.run(urls)
	
	