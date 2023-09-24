import aiohttp_jinja2
from aiohttp import web

import youtube
import Q


@aiohttp_jinja2.template('index.html')
async def getreq(_):
	return {}

async def songreq(request):
	data = await request.post()
	try:
		song =	data['song']
		results = await youtube.search(song)
		return web.json_response(results)
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Enter a song') from e

async def add(request):
	data = await request.post()
	try:
		video_id = data["videoId"]
		Q.enqueue(video_id)
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Error adding selection to queue') from e
