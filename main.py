#!/usr/bin/env python
import asyncio
import os
import hashlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import from_url

import middleware
import Q
import routes
import logger as log


logger = log.get_logger(__name__)

async def init_persistent(persistent, file_path="media/.admin_pass"):
	if os.environ.get("DISABLE_AUTH"):
		return False
	elif not os.path.exists(file_path):
		proc = await asyncio.create_subprocess_shell(
			f"openssl rand -base64 12 > {file_path}",
			stderr=asyncio.subprocess.PIPE
		)
		_, stderr = await proc.communicate()
		if stderr:
			logger.error("Error while creating admin", stderr.decode())
			return False
	with open(file_path) as f:
		admin_pass = f.read().strip()
		logger.info("admin password %s", admin_pass)
		await persistent.set(
			"admin_password", 
			hashlib.sha256(admin_pass.encode()).hexdigest()
		)
	return True


async def main():
	q = Q.QM()
	app = web.Application()
	aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
	app["redis"] = "redis://127.0.0.1:6379"
	redis = await from_url(app["redis"])
	app["auth_enabled"]  = await init_persistent(redis)
	storage = RedisStorage(redis)
	setup(app, storage)
	app.middlewares.append(middleware.unset_cookies)
	app.add_routes([
		web.get('/', routes.getreq), 
		web.post('/', routes.songreq),
		web.post('/add', routes.add),
		web.get('/qinfo', routes.QWatcher),
		web.post('/setuser', routes.add_username),
		web.get('/toggle', routes.toggle_playing),
		web.delete("/remove/{qpos:\d+}", routes.remove), 
		web.static('/static', "static"),
		web.get("/admin", routes.getadmin),
		web.post("/admin/auth", routes.authenticate)
	])
	app.on_shutdown.append(middleware.on_shutdown)
	app["websockets"] = {}
	app["Q"] = q

	partyq = asyncio.to_thread(Q.partyQ, q)
	task = asyncio.create_task(partyq)
	app["partyq"] = task
	return app

if __name__ == "__main__":
	asyncio.run(main())
