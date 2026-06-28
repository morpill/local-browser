from core.registry import App, AppRegistry
from utils.validation.validate_target import validate_target
from errors import Invalid
import requests

def post(identifier: str, path: str = '', **kwargs):
    app: App = AppRegistry.get(identifier)
    
    if validate_target(app):
        r = requests.post(f'{app.target}/{path}', **kwargs)
        return r
    
    return Invalid()