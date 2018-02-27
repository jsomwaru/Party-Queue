import aiohttp_jinja2
import jinja2
import json
from aiohttp import web
from songreq import SongReq

@aiohttp_jinja2.template('index.html')	
async def index(request):
	#response_obj = { 'status': 'success', 'message':'good' }
	#return web.Response(text=json.dumps(response_obj), status=200)
	return{}
	
async def do_post(request):
	response_obj = { 'status': 'success', 'message':'good' }
	response_bad = { 'status': 'notgood', 'message':'bad'  }
	data = await request.post()
	try:
		artist, song = data['artist'], data['song']
		proxy_url = SongReq(artist, song)
		proxy_url.formatUrl()
		#Write url to queue file 
		with open (file, proxy_url) as f:
			f.write(proxy_url)
		#redirect to index 	
		raise web.HTTPFound('/')
		return web.Response(text=json.dumps(response_obj), status=200)	
		#bullshit i dont know 
	except (KeyError, TypeError, ValueError) as e:
		raise web.HTTPBadRequest(
			text = 'Enter a song and title') from e
		return web.Response(text=json.dumps(response_bad), status=500)