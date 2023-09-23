import aiohttp_jinja2
from aiohttp import web 

@aiohttp_jinja2.template('index.html')
async def getreq(request):
	return {}

async def songreq(request):
	data = await request.post()
	try:
		song =	data['song']
		print (song)
	except (KeyError, TypeError, ValueError) as e:
		raise web.HTTPBadRequest(
		text = 'Enter a artist and song') from e
	return web.HTTPFound('/')
