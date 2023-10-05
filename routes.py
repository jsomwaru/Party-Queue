import json

import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
from aiohttp_session import get_session

import Q
import youtube


@aiohttp_jinja2.template('index.html')
async def getreq(_):
	return {}


async def songreq(request):
	data = await request.post()
	session = await get_session(request)
	try:
		session = await get_session(request)
		song =	data['song']
		results = await youtube.search(song)
		session["cache"] = results
		return web.json_response(results)
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Enter a song') from e


async def add(request):
	data = await request.json()
	session = await get_session(request)
	try:
		video_id = data["videoId"]
		metadata = None
		print(type(session.get("cache")))
		for entry in session.get("cache"):
			entry_video = entry.get('videoId')
			if video_id == entry_video:
				metadata = entry
		print(video_id, metadata)
		if video_id and metadata:
			Q.enqueue(metadata)
		return web.HTTPAccepted()
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Error adding selection to queue') from e


async def QWatcher(request):
	session = await get_session(request)
	request.app["websockets"][session.identity] = ws
	ws = WebSocketResponse()
	await ws.prepare(request)
	conn = request.app["db"]
	conn.execute(f"SELECT song, requestor, status FROM Q WHERE status in ('playing', 'waiting')")
	results = conn.fetchall()
	ws.send_str(json.dumps(results))
