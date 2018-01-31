from tornado import ioloop
from tornado import web
from tornado import gen 

class MainHandler(web.RequestHandler):
	@gen.coroutine
	def get(self):
		self.render('index.html')
	
	@gen.coroutine
	def post(self):
		title = get_body_argument("artist")
		song  = get_body_argument("song")
		
def make_app():
	return web.Application([
		(r"/", MainHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	ioloop.IOLoop.current().start()