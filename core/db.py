from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

db_path = BASE_DIR.parent / 'browser.db'

Base = declarative_base()

class App(Base):
    __tablename__ = 'apps'
    
    id = Column(Integer, primary_key=True)
    identifier = Column(String, unique=True)
    name = Column(String)
    target = Column(String)
    
class CacheEntry(Base):
    __tablename__ = 'cache_entry'
    
    id = Column(Integer, primary_key=True)
    identifier = Column(String)
    path = Column(String)
    timestamp = Column(DateTime, server_default=func.now())
    
    content = Column(LargeBinary, nullable=False)
    headers = Column(String)
    
class Cookie(Base):
    __tablename__ = 'cookies'

    id = Column(Integer, primary_key=True)

    app_id = Column(Integer, ForeignKey('apps.id'))
    path = Column(String, default='/')

    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    expires = Column(DateTime, nullable=True)
    max_age = Column(Integer, nullable=True)

    secure = Column(Boolean, default=False)
    http_only = Column(Boolean, default=False)
    same_site = Column(String, nullable=True)

    created = Column(DateTime, server_default=func.now())
    
engine = create_engine(f'sqlite:///{db_path}')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
