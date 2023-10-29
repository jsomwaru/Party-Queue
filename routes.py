import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
from aiohttp import WSCloseCode
from aiohttp_session import get_session

import logger as log
import Q
import youtube


logger = log.get_logger(__name__)

def spam_detector(request: dict, q: Q.QM):
    duplicates = q.get_by_videoid(request["videoId"])
    queue = q.get_queue()
    logger.info("Found %d duplicates", len(duplicates))
    if len(queue) == 0 or (len(duplicates) / (len(queue) + 1) < 0.05 and queue[-1].get("videoId") != request["videoId"]):
        return True 
    return False


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
			if spam_detector(metadata, request.app["Q"]):
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
		return web.HTTPAccepted(text="Pause")
	else: # Play
		Q.CONTROL.set()
		logger.info("%s started the Q", session.get("username", session.identity))
		return web.HTTPAccepted(text="play")


async def on_shutdown(app):
	for ws in app['websockets'].values():
		try:
			await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')
		except Exception:
			pass

async def remove(request: web.Request):
    try:
        qpos = request.match_info["qpos"]
        request.app["Q"].remove(int(qpos))
        return web.HTTPAccepted()
    except Exception as e:
        logger.error(e)
        return web.HTTPError(text="Failure to remove")

@web.middleware
async def unset_cookies(request, handler):
    resp: web.HTTPAccepted = await handler(request)
    session = await get_session(request)
    username = session.get("username")
    if not username:
        resp.del_cookie("username")
    return resp
	