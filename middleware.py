from aiohttp.web import middleware


@middleware
async def setup_session():
    pass 

@middleware
async def cache(request, handler):
    request.app["cache"][resp["sesion-id"]].clear()
    resp = await handler(request)
    return resp
