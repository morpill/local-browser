from core.registry import App, AppRegistry
from utils.validation.validate_target import validate_target
from errors import Invalid
import requests

def delete(identifier: str, path: str = ''):
    app: App = AppRegistry.get(identifier)
    
    if validate_target(app):
        
        r = requests.delete(f'{app.target}/{path}')
        return r
    
    return Invalid()