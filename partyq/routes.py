import urllib.parse 

from hashlib import sha256

import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
from aiohttp_session import get_session

import redis.asyncio as redis

from partyq import logger as log
from partyq import middleware
from partyq import Q
from partyq import youtube

AUTH = "authenticated"

logger = log.get_logger(__name__)


@aiohttp_jinja2.template('index.html')
async def getreq(request):
	await get_session(request) # start or get session
	return {}


@aiohttp_jinja2.template('admin.html')
async def getadmin(request):
    try:
        await get_session(request) # start or get session
        return {}
    finally:
        return {}


async def authenticate(request):
	try:
		if request.app["admin_enabled"]:
			session = await get_session(request)
			data = await request.post()
			password = data["password"]
			password = urllib.parse.unquote(password)
			conn = redis.from_url(request.app["redis"])
			admin_pass = await conn.get("admin_password")
			if sha256(password.encode()).hexdigest() == admin_pass.decode():
				session[AUTH] = True
				res = web.HTTPAccepted()
				res.set_cookie("authenticated", "1")
				return res
			return web.HTTPUnauthorized()
		return web.HTTPOk()
	except Exception as e:
		logger.error(e)
		return web.HTTPBadRequest()

        
async def songreq(request):
	data = await request.post()
	session = await get_session(request)
	try:
		session = await get_session(request)
		song =	data['song']
		results = await youtube.search(song)
		results = [res for res in results if "videoId" in list(res.keys())]
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
		cache = session.get("cache")
		if not cache:
			if video_id == "undefined":
				raise KeyError
			cache = await youtube.search(video_id)
		metadata = next(entry for entry in cache if entry.get("videoId"))
		for entry in cache:
			entry_video = entry.get('videoId')
			if video_id == entry_video:
				metadata = entry
		if video_id and metadata and video_id != "undefined":
			metadata["requestor"] = session.get("username", "anonymous")
			if middleware.spam_detector(metadata, request.app["Q"]):
				request.app["Q"].enqueue(metadata)
				logger.info("Added song %s to queue", metadata["title"])
				logger.debug(str(metadata))
			else:
				return web.HTTPBadRequest(reason="Spam Detected")
		return web.HTTPAccepted()
	except KeyError as e:
		logger.error("Key error")
		raise web.HTTPBadRequest(text = 'Error adding selection to queue') from e


async def QWatcher(request):
	session = await get_session(request)
	resp = WebSocketResponse()
	request.app["websockets"][session.identity] = resp
	logger.info("Creating new websocket")
	await resp.prepare(request)
	await resp.send_json(request.app["Q"].get_queue())
	try:
		async for _ in resp:
			await resp.send_json(request.app["Q"].get_queue())
		return resp
	finally:
		logger.info("Client %s disconnected", session.identity)
		await request.app["websockets"][session.identity].close()


async def add_username(request):
    session = await get_session(request)
    try:
        data = await request.post()
        username = data["username"]
        session["username"] = username
        logger.info("username %s", username)
        resp = web.HTTPAccepted()
        resp.set_cookie("username", "1")
        return resp
    except Exception as e:
        logger.error("ERROR while submmiting log %s", e)
        raise web.HTTPInternalServerError(text="An error occured") from e


async def toggle_playing(request):
	session = await get_session(request)
	if Q.CONTROL.is_set(): # Pause
		Q.CONTROL.clear()
		logger.info("%s paused the Q", session.get("username", session.identity))
		return web.HTTPAccepted(text="Play")
	else: # Play
		Q.CONTROL.set()
		logger.info("%s started the Q", session.get("username", session.identity))
		return web.HTTPAccepted(text="Pause")


async def remove(request: web.Request):
    try:
        session = await get_session(request)
        if session.get(AUTH):
            qpos = request.match_info["qpos"]
            request.app["Q"].remove(int(qpos))
            user = session.get("username", session.identity)
            logger.info("User %s removed song at pos %s", user, qpos)
            return web.HTTPAccepted(text=f"Song Removed at pos {qpos}")
    except Exception as e:
        logger.error(e)
        return web.HTTPError(text="Failure to remove")
