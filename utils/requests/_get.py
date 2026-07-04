from core.registry import App, AppRegistry
from utils.validation.validate_target import validate_target
from errors import Invalid
from core.caching import Cache, is_cacheable, CachedResource, CacheEntry, get_max_age, is_cached_valid
from core.cookies import Cookies
from config import config
import json
import requests

def get(identifier: str, path: str = ''):
    app: App = AppRegistry.get(identifier)    

    if validate_target(app):
        _cached = _use_cached(identifier) 
        rval = _cached       

        if not rval:

            try:
                r = requests.get(f'{app.target}/{path}')
                rval = r
            except requests.exceptions.ConnectionError:
                return Invalid()
            
            if config.get('CACHING', True) and r.ok and is_cacheable(r) and not _cached:
                Cache.cache(identifier, path, r.content, dict(r.headers))

        return rval
                
    return Invalid()

def _use_cached(
    identifier: str, 
    path: str = '', 
    max_age: int | None = None
):
    if config.get('CACHING', True) is False:
        return None
    
    result: CacheEntry = Cache.get(identifier, path)
    if not result:
        return None
    
    headers = json.loads(result.headers)
    
    if not max_age:
        max_age = get_max_age(headers.get('Content-Type', 'text/plain'))
        
    return CachedResource(
        result.identifier,
        result.path,
        result.timestamp,
        result.content,
        headers
    ) if is_cached_valid(result, max_age) else None
    
def cookies(r: Invalid | CachedResource | requests.Response, identifier: str, path: str):
    if not 'Set-Cookie' in r.headers:
        return
    
    Cookies.set(
        app_identifier=identifier,
        path=path,
        
    )