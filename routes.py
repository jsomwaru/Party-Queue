import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
from aiohttp import WSCloseCode
from aiohttp_session import get_session

import db
import logger as log
import Q
import youtube


logger = log.get_logger(__name__)

@aiohttp_jinja2.template('index.html')
async def getreq(request):
	await get_session(request) # start or get session
	return {}


async def songreq(request):
	data = await request.post()
	session = await get_session(request)
	try:
		session = await get_session(request)
		song =	data['song']
		results = await youtube.search(song)
		session["cache"] = [res for res in results if "videoId" in list(res.keys())]
		return web.json_response(results)
	except KeyError as e:
		raise web.HTTPBadRequest(text = 'Enter a song') from e


async def add(request):
	data = await request.json()
	session = await get_session(request)
	try:
		video_id = data["videoId"]
		metadata = None
		cache = session.get("cache")
		if not cache:
			if video_id == "undiefined":
				raise KeyError
			cache = await youtube.search(video_id)
		for entry in cache:
			entry_video = entry.get('videoId')
			if video_id == entry_video:
				metadata = entry
		if video_id and metadata and video_id != "undefined":
			metadata["requestor"] = session.identity
			Q.enqueue(metadata)
			logger.info("Added song %s to queue", metadata["title"])
			logger.debug(str(metadata))
			db.add_song(metadata)
			logger.info("Saved song metadata")
		return web.HTTPAccepted()
	except KeyError as e:
		logger.error("Key error")
		raise web.HTTPBadRequest(text = 'Error adding selection to queue') from e


async def QWatcher(request):
	session = await get_session(request)
	resp = WebSocketResponse()
	request.app["websockets"][session.identity] = resp
	logger.info("creating new websocket")
	await resp.prepare(request)
	# results = db.get_by_status("enqueue")
	await resp.send_json(Q.Q)
	try:
		async for _ in resp:
			# results = db.get_by_status("enqueue")
			await resp.send_json(Q.Q)
		return resp
	finally:
		logger.info("Client %s disconnected", session.identity)
		await request.app["websockets"][session.identity].close()


async def add_username(request):
	session = await get_session(request)
	data = await request.post()
	username = data["username"]
	db.add_session(session, username)


async def on_shutdown(app):
	for ws in set(app.get('websockets', [])):
		try:
			await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')
		except Exception:
			pass

