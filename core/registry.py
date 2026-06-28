from core.db import Session, App
import pathlib as pl
import re
from urllib.parse import urlparse

IDENTIFIER_PATTERN = re.compile(r'^[a-z0-9]+\.[a-z0-9]+$')

class InvalidAppData(Exception):
    pass

class FailedToRegisterApp(Exception):
    pass

def _validate_data(identifier, name, target):
    if not IDENTIFIER_PATTERN.match(identifier):
        return False
    if len(identifier) >= 50 or len(name) >= 50:
        return False
    try:
        result = urlparse(target)
        return result.scheme in ('http', 'https') and bool(result.netloc)
    except:
        return False

def _register_app(app: App):
    db = Session()
    db.add(app)
    db.commit()
    
def _get_apps():
    db = Session()

    try:
        return db.query(App).all()
    finally:
        db.close()
        
def _get_app(identifier: str) -> App:
    db = Session()
    
    try:
        result = db.query(App).filter_by(identifier=identifier).all()
        return result[0] if len(result) > 0 else None
    finally:
        db.close()
    
def _reset_db():
    db = Session()
    db.query(App).delete()
    db.commit()
    
def _delete_app(identifier: str ) -> None:
    db = Session()
    db.query(App).filter_by(identifier=identifier).delete()
    db.commit()

class AppRegistry:
    @staticmethod
    def register(identifier: str, name: str, target: str):
        if not _validate_data(identifier, name, target):
            raise InvalidAppData('The app data you entered are invalid. See documentation.')
        
        app = App(
            identifier=identifier,
            target=target,
            name=name
        )
        
        try:
            _register_app(app)
        except Exception as e:
            raise FailedToRegisterApp(f'Failed to register app {identifier}. Exception:\n{e}')
    
    @staticmethod
    def get_all() -> list[App]:
        return _get_apps()
    
    @staticmethod
    def get(identifier: str) -> App:
        return _get_app(identifier)
    
    @staticmethod
    def delete(identifier: str) -> None:
        return _delete_app(identifier)
               
        