from core.registry import App
from core.manifest import ManifestParser as Parser, ManifestCache as Cache

cache = Cache()

def _check_cached(app: App) -> bool | None:
    return cache.get(app.identifier)

def validate_target(app: App):
    if not app:
        return False
    
    cached = _check_cached(app)
    
    if cached:
        return True
    
    if cached is None:
        manifest = Parser.parse(Parser.get_manifest(app))
        if Parser.verify_signature(manifest) and Parser.check(manifest, identifier=app.identifier):
            cache.set(app.identifier, True)
            return True
        
        cache.set(app.identifier, False)
        return False
    
    return False