import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
import Q
import youtube


@aiohttp_jinja2.template('index.html')
async def getreq(_):
	return {}


async def songreq(request):
	data = await request.post()
	session = await get_session(request)
	print(session)
	try:
		session = await get_session(request)
		song =	data['song']
		results = await youtube.search(song)
		request.app["cache"] = { **next(res for res in results) }
		return web.json_response(results)
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Enter a song') from e


async def add(request):
	data = await request.json()
	try:
		video_id = data["videoId"]
		request.app["cache"][video_id]
		Q.enqueue(video_id)
		return web.HTTPAccepted()
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Error adding selection to queue') from e
