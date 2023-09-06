# ==============================================================================
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By: Abhisek Ashirbad Sethy
# Created Date: 05/09/2023 (DD/MM/YYYY)
# Copyright: Apache License v2.0
# ==============================================================================

# Imports
import app.utils.config as config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from requests_cache import CachedSession
from app.db.retry_query import RetryingQuery
import databases
import aiosqlite

def get_engine(uri):
    options = {
        "echo": config.DB_ECHO,
        "execution_options": {
            "autocommit": config.DB_AUTOCOMMIT, 
            "autoflush": config.DB_AUTOFLUSH
            }
    }
    return create_engine(uri, **options)

db_session = scoped_session(sessionmaker())
engine = get_engine(config.DB_URL)
cache_session = CachedSession('http_cache', allowable_methods=['GET', 'POST'], backend='sqlite', \
                               stale_while_revalidate=True)


def init_session():
    db_session.configure(bind=engine, query_cls=RetryingQuery)
    from app.db.db_tables import Base
    Base.metadata.create_all(engine)
    

async def get_db():
    db = await aiosqlite.connect(config.DB_URL)
    try:
        yield db
    finally:
        db.close()