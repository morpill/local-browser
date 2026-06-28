from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions
from utils.requests import get, post, delete
import asyncio
import threading
from errors import Invalid
from utils.processing.html import HTMLProcessor
import config as cfg
from functools import partial
import asyncio
import socket

PORT = cfg.config.get('PROXY_PORT', 5000)
BASE = f'http://localhost:{PORT}'

def _check_port(port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex(('127.0.0.1', port))
        return result == 0
    finally:
        sock.close()
    

def _make_base(identifier: str):
    return f'{BASE}/{identifier}/'

def _get_identifier(request) -> str:
    host = request.headers.get('Host', '')
    return host.split('.localhost')[0]

def _parse_content_type(content_type: str) -> tuple[str, str]:
    parts = content_type.split(';')
    mime = parts[0].strip()
    charset = None
    for part in parts[1:]:
        part = part.strip()
        if part.startswith('charset='):
            charset = part.split('=', 1)[1].strip()
    return mime, charset

async def proxy_route_get(request):
    identifier = _get_identifier(request)
    path = request.match_info['path']
    query_string = request.query_string
    full_path = f'{path}?{query_string}' if query_string else path
    
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, partial(get, identifier, full_path))
    
    if isinstance(r, (Invalid)):
        return web.Response(status=404, text=f'App "{identifier}" not found')
    
    content_type = r.headers.get('Content-Type', '')
    body = HTMLProcessor.process(r.content, identifier) if 'text/html' in content_type else r.text
    mime, charset = _parse_content_type(content_type)
    
    return web.Response(body=body, content_type=mime, charset=charset, headers={'X-Frame-Options': 'ALLOWALL'})
    
async def proxy_route_post(request):
    identifier = _get_identifier(request)
    path = request.match_info['path']
    query_string = request.query_string
    full_path = f'{path}?{query_string}' if query_string else path
    body = await request.read()
    headers = dict(request.headers)

    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, partial(post, identifier, full_path))

    
    if isinstance(r, Invalid):
        return web.Response(status=404, text=f'App "{identifier}" not found')
    
    content_type = r.headers.get('Content-Type', '')
    body = HTMLProcessor.process(r.content, _make_base(identifier)) if 'text/html' in content_type else r.content
    mime, charset = _parse_content_type(content_type)
    
    return web.Response(body=body, content_type=mime, charset=charset)
    
async def proxy_route_delete(request):
    identifier = _get_identifier(request)
    path = request.match_info['path']
    query_string = request.query_string
    full_path = f'{path}?{query_string}' if query_string else path
    
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, partial(delete, identifier, full_path))

    
    if isinstance(r, Invalid):
        return web.Response(status=404, text=f'App "{identifier}" not found')
    
    content_type = r.headers.get('Content-Type', '')
    body = HTMLProcessor.process(r.content, _make_base(identifier)) if 'text/html' in content_type else r.content
    mime, charset = _parse_content_type(content_type)
    
    return web.Response(body=body, content_type=mime, charset=charset)

async def startpage(request):
    pass

app = web.Application()

resource_get = app.router.add_resource('/{path:.*}')
resource_post = app.router.add_resource('/{path:.*}')
resource_delete = app.router.add_resource('/{path:.*}')
resource_startpage = app.router.add_resource('/')

route_get = resource_get.add_route('GET', proxy_route_get)
route_post = resource_post.add_route('POST', proxy_route_post)
route_delete = resource_delete.add_route('DELETE', proxy_route_delete)
route_startpage = resource_startpage.add_route('GET', startpage)

from aiohttp_cors import CorsViewMixin, ResourceOptions
import aiohttp_cors

cors = aiohttp_cors.setup(app, defaults={
    f'http://localhost:{PORT}': ResourceOptions(
        allow_credentials=True,
        expose_headers='*',
        allow_headers='*',
        allow_methods=['GET', 'POST', 'DELETE']
    ),
    f'http://127.0.0.1:{PORT}': ResourceOptions(
        allow_credentials=True,
        expose_headers='*',
        allow_headers='*',
        allow_methods=['GET', 'POST', 'DELETE']
    ),
})

def start(port: int = PORT, debug: bool = False):
    if _check_port(port) == 0:
        async def _run():
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', port)
            await site.start()
            await asyncio.Event().wait()
        
        if debug:
            print(f'[info] proxy running on 127.0.0.1:{port}.')
        thread = threading.Thread(target=asyncio.run, args=(_run(),), daemon=True)
        thread.start()
    else:
        print(f'[warning] port {port} is blocked. Could not start proxy. Maybe it\'s already running?')