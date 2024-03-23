from aiohttp import WSCloseCode
from aiohttp import web
from aiohttp_session import get_session

from partyq import Q
from partyq import logger as log

logger = log.get_logger(__name__)

async def on_shutdown(app):
    for ws in app['websockets'].values():
        try:
            await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')
        except Exception:
            pass

def spam_detector(request: dict, q: Q.QM):
    duplicates = q.get_by_videoid(request["videoId"])
    queue = q.get_queue()
    logger.info("Found %d duplicates", len(duplicates))
    if len(queue) == 0 or (len(duplicates) / (len(queue) + 1) < 0.05 and queue[-1].get("videoId") != request["videoId"]):
        return True 
    return False

@web.middleware
async def unset_cookies(request, handler):
    resp: web.HTTPAccepted = await handler(request)
    session = await get_session(request)
    # Unset username
    username = session.get("username")
    if not username:
        resp.del_cookie("username")
    # Unset authenticated
    authenticated = session.get("authenticated")
    if not authenticated:
          resp.del_cookie("authenticated")
    return resp
