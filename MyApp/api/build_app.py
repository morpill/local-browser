from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import base64
import json
import pathlib

class App:
    def __init__(
        self,
        name: str,
        user: str,
        version: str = '1.0.0'
    ):
        self.name: str = name
        self.user: str = user
        self.version: str = version
        self.identifier: str = f'{name.lower()}.{user}'
        self.manifest = {
            'name': name,
            'identifier': self.identifier,
            'version': version
        }
        self._sign()
        
    def _sign(self):
        private_key = ed25519.Ed25519PrivateKey.generate()
        
        manifest_bytes = json.dumps(self.manifest).encode()
        signature = private_key.sign(manifest_bytes)
        
        public_key_bytes = private_key.public_key().public_bytes(
            Encoding.Raw,
            PublicFormat.Raw
        )
        
        self.manifest['public_key'] = base64.b64encode(public_key_bytes).decode()
        self.manifest['signature'] = base64.b64encode(signature).decode()
        
    def _save_manifest(self):
        with open('manifest.json', 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2)
        
