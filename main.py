#!/usr/bin/env python
import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import from_url

import routes
import Q


async def main():
	q = Q.QM()
	app = web.Application()
	aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
	redis = await from_url("redis://127.0.0.1:6379")
	storage = RedisStorage(redis)
	setup(app, storage)
	app.add_routes([
		web.get('/', routes.getreq), 
		web.post('/', routes.songreq),
		web.post('/add', routes.add),
		web.get('/qinfo', routes.QWatcher),
		web.post('/setuser', routes.add_username)
	])
	app.on_shutdown.append(routes.on_shutdown)
	app["websockets"] = {}
	app["Q"] = q

	partyq = asyncio.to_thread(Q.partyQ, q)
	task = asyncio.create_task(partyq)
	app["partyq"] = task
	return app

if __name__ == "__main__":
	asyncio.run(main())
