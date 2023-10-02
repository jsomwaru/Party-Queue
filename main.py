#!/usr/bin/env python
import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web


import routes
import Q

if __name__ == "__main__":
	async def main():
		app = web.Application()
		aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
		app.add_routes([
			web.get('/', routes.getreq), 
			web.post('/', routes.songreq),
			web.post('/add', routes.add)
		])
		await asyncio.gather(
			web._run_app(app, host='0.0.0.0', port=80),
			asyncio.to_thread(Q.partyQ)
		)
		
	asyncio.run(main())
