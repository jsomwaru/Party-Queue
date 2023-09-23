#!/usr/bin/env python
import aiohttp_jinja2
import jinja2
from aiohttp import web

import routes

if __name__ == "__main__":	
	app = web.Application()
	aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
	app.add_routes([web.get('/', routes.getreq),web.post('/', routes.songreq)])
	web.run_app(app, host='0.0.0.0', port=80)
