import asyncio
import json
import urllib.parse
from functools import partial
from hashlib import sha256

import aiohttp
import aiohttp_jinja2
import redis.asyncio as redis
from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
from aiohttp_session import get_session

from partyq import Q, config
from partyq import logger as log
from partyq import middleware, youtube
from partyq.device import DeviceManager

logger = log.get_logger(__name__)


@aiohttp_jinja2.template('index.html')
async def getreq(request: web.Request):
    await get_session(request) # start or get session
    return {}


@aiohttp_jinja2.template('admin.html')
async def getadmin(request: web.Request):
    try:
        await get_session(request) # start or get session
        return {}
    finally:
        return {}


async def authenticate(request: web.Request):
    try:
        if request.app["admin_enabled"]:
            session = await get_session(request)
            data = await request.post()
            password = data["password"]
            password = urllib.parse.unquote(password)
            conn = redis.from_url(request.app["redis"])
            admin_pass = await conn.get("admin_password")
            if sha256(password.encode()).hexdigest() == admin_pass.decode():
                session[config.AUTH] = True
                res = web.HTTPAccepted()
                res.set_cookie("authenticated", "1")
                return res
            return web.HTTPUnauthorized()
        return web.HTTPOk()
    except Exception as e:
        logger.error(e)
        return web.HTTPBadRequest()


async def songreq(request: web.Request):
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


async def add(request: web.Request):
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


async def QWatcher(request: web.Request):
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


async def add_username(request: web.Request):
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


async def toggle_playing(request: web.Request):
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
        if session.get(config.AUTH):
            qpos = request.match_info["qpos"]
            request.app["Q"].remove(int(qpos))
            user = session.get("username", session.identity)
            logger.info("User %s removed song at pos %s", user, qpos)
            return web.HTTPAccepted(text=f"Song Removed at pos {qpos}")
    except Exception as e:
        logger.error(e)
        return web.HTTPError(text="Failure to remove")


async def update_authentication(request: web.Request):
    data = await request.json()
    with open(youtube.BROWSER_FILE, "w+") as f:
        f.write(json.dumps(data))
    return web.HTTPAccepted(text="Credentials Updated")


async def list_devices(request: web.Request):
    # TODO Add authentication
    try:
        stream = request.query.get("stream")
        logger.info("Getting streaming %s", str(stream))
        device_manager = request.app["DeviceManager"]
        session = await get_session(request)
        if not stream:
            logger.info("Listing devices")
            # device_manager.list_devices()
            device_manager.list_devices()
            device_manager.run_delegate()
            data = device_manager.get_devices()
            # logger.debug(f"%d available devices", len(data["devices"]))
            return web.json_response(data=data, content_type="application/json")
        elif stream == "true":
            logger.info("Listing devices streaming")
            event = asyncio.Event()
            event.clear()
            resp = WebSocketResponse()
            await device_manager.list_devices_streaming(event)
            await resp.prepare(request)
            device_callback = partial(middleware.send_device_info, resp)
            request.app["websockets"][f"device:{session}"] = resp
            try:
                task: asyncio.Task = asyncio.create_task(device_manager.get_devices(device_callback))
                task.add_done_callback(request.app["background_tasks"].discard)
                request.app["background_tasks"].add(task)
                async for req in resp:
                    if req.type == aiohttp.WSMsgType.TEXT:
                        data = await req.json() 
                    if data.get("quit"):
                        event.set()
                        raise Exception("Client diconnected")
            finally:
                device_manager.scan_task.cancel()
                task.cancel()
                await resp.close()
                logger.exception("")
                return web.HTTPSuccessful()
    except Exception:
        logger.exception("error")
        return web.HTTPInternalServerError(text="Error listing devices")


async def set_device(request: web.Request):
    # TODO Add authentication
    # TODO Handle set_device while song is currently playing
    did = request.match_info["did"]
    if not did:
        return web.HTTPBadRequest(text="No device provided")
    d = DeviceManager()
    succ = await d.set_playback_device(device_id=did)
    if not succ:
        err = {"message": f"Deivce {did} not found"}
        logger.info(f"{did} {d.device_dict()}")
        return web.HTTPNotFound(text=json.dumps(err))
    device_dict = d.current_device.asdict()
    device_dict.update({"msg": "Current Device Set Sucessfully"})
    return web.json_response(data=device_dict, content_type="application/json")
    