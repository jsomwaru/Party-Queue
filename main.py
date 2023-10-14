#!/usr/bin/env python
import asyncio

from datetime import timedelta

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import from_url

import db
import routes
import Q



async def main():
	app = web.Application()
	aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
	redis = await from_url("redis://127.0.0.1:6379")
	print(timedelta(days=30).seconds)
	# storage = RedisStorage(redis, max_age=int(timedelta(days=30).seconds))
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
	db.setup_db()
	# await asyncio.gather(
	#   web._run_app(app, host='0.0.0.0', port=80),
	# 	asyncio.to_thread(Q.partyQ)
	# )
	partyq = asyncio.to_thread(Q.partyQ)
	task = asyncio.create_task(partyq)
	app["partyq"] = task
	return app

if __name__ == "__main__":
	asyncio.run(main())
