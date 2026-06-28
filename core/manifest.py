import json
import requests
from core.db import App
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from datetime import timedelta, datetime

class ManifestNotFound(Exception):
    pass

class InvalidSignature(Exception):
    pass

REQUIRED_KEYS = [
    'identifier',
    'name', 
    'public_key', 
    'signature'
]

class ManifestParser:
    @staticmethod
    def parse(manifest: str):
        return json.loads(manifest)
    
    @staticmethod
    def get_manifest(app: App):
        try:
            r = requests.get(app.target + '/manifest.json')
        except requests.exceptions.ConnectionError:
            return '{}'
        if not r.ok:
            raise ManifestNotFound('Source has no manifest. Make sure the manifest is provided at /manifest.json')
        return r.text
    
    @staticmethod
    def check(manifest: dict, **kwargs):
        for key, value in kwargs.items():
            if manifest.get(key) != value:
                return False
        return True
    
    @staticmethod
    def verify_signature(manifest: dict):
        try:
            signature = base64.b64decode(manifest['signature'])
            public_key_bytes = base64.b64decode(manifest['public_key'])
            
            manifest_to_verify = {
                k: v for k, v in manifest.items()
                if k not in ('signature', 'public_key')
            }
            
            manifest_bytes = json.dumps(manifest_to_verify).encode()
            
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        except:
            return False

        try:
            public_key.verify(signature, manifest_bytes)
            return True
        except Exception:
            return False
            # raise InvalidSignature(f'Manifest is invalid for {manifest.get('identifier')}.')
        
REQUIRED_MANIFEST_CACHE_KEYS = [
    'identifier',
    'timestamp',
    'safe'
]        
        
class ManifestCache:
    def __init__(self):
        self.cache: dict[str, dict[str, bool | datetime]] = {}
    
    def get(self, identifier: str) -> bool | None:
        entry = self.cache.get(identifier)
        if not entry:
            return None
        if datetime.now() - entry['checked'] > timedelta(seconds=60):
            del self.cache[identifier]
            return None
        return entry['safe']
    
    def set(self, identifier: str, safe: bool):
        self.cache[identifier] = {
            'safe': safe,
            'checked': datetime.now()
        }