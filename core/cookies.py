from core.db import Cookie as CookieModel, Session
from core.registry import AppRegistry
from datetime import datetime 

def _set_cookie(cookie: CookieModel):
    db = Session()
    try:
        db.add(cookie)
    finally:    
        db.commit()
    
def _get_all_cookies():
    db = Session()
    try:
        return db.query(CookieModel).all()
    finally:
        db.close()

def _get_app_id(identifier: str) -> int:
    return AppRegistry.get(identifier).id

class Cookies:
    @staticmethod
    def set(
        app_identifier: str,
        path: str,
        name: str,
        value: str,
        expires: datetime | None = None,
        max_age: int | None = None,
        secure: bool = False,
        http_only: bool = False,
        same_site: str | None = None
    ):
        cookie = CookieModel(
            app_id=_get_app_id(app_identifier),
            path=path,
            name=name,
            value=value,
            expires=expires,
            max_age=max_age,
            secure=secure,
            http_only=http_only,
            same_site=same_site
        )

        return _set_cookie(cookie)
    
    def get_all():
        return _get_all_cookies()