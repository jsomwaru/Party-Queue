import aiohttp_jinja2
import jinja2

from aiohttp import web
from views import do_post, index

app = web.Application()
aiohttp_jinja2.setup(app, 
loader=jinja2.FileSystemLoader('templates'))
	
app.router.add_get('/', index)
app.router.add_post('/', do_post)

web.run_app(app, host='127.0.0.1', port=8000,) 
