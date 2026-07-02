from core.db import CacheEntry, Session
from config import config
from requests import Response
from dataclasses import dataclass
import json
from datetime import datetime, timedelta

def _get_cache():
    db = Session()
    try:
        return db.query(CacheEntry).all()
    finally:
        db.close()

def _get_cache_entry(identifier: str, path: str):
    db = Session()
    try:
        return db.query(CacheEntry).filter_by(identifier=identifier.lower(), path=path.lower()).first()
    finally:
        db.close()
    
def _add_entry(entry: CacheEntry):
    db = Session()
    db.query(CacheEntry).filter_by(identifier=entry.identifier, path=entry.path.lower()).delete()
    db.add(entry)
    db.commit()
    
def _clear_cache():
    db = Session()
    db.query(CacheEntry).delete()
    db.commit()
    
def is_cacheable(response: Response):
    headers = response.headers
    cache_control = headers.get('Cache-Control', '').lower()
    
    if 'no-store' in cache_control:
        return False
    
    if 'private' in cache_control:
        return False
    
    if 'Set-Cookie' in headers:
        return False
    
    return True

def get_max_age(content_type: str) -> int:
    mime = content_type.split(';')[0].strip().lower()
    
    return config['CACHING_MAX_AGE'].get(
        mime,
        60
    )
    
def is_cached_valid(entry: CacheEntry, max_age: int):
    expires_at = entry.timestamp + timedelta(seconds=max_age)

    return datetime.utcnow() < expires_at

class Cache:
    @staticmethod
    def all(*args, **kwargs):
        return _get_cache(*args, **kwargs)
    
    @staticmethod
    def get(*args, **kwargs):
        return _get_cache_entry(*args, **kwargs)
    
    @staticmethod
    def cache(identifier: str, path: str, content: str, headers: dict, *args, **kwargs):
        entry = CacheEntry(
            identifier=identifier,
            path=path,
            content=content,
            headers=json.dumps(headers)
        )
        return _add_entry(entry, *args, **kwargs)
    
    @staticmethod
    def clear(*args, **kwargs):
        return _clear_cache(*args, **kwargs)

@dataclass        
class CachedResource:
    identifier: str
    path: str
    timestamp: str
    text: bytes
    headers: dict 