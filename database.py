import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


USERNAME = os.getenv("PERSISTENT_LOG_DB_USERNAME")
PASSWORD = os.getenv("PERSISTENT_LOG_DB_PASSWORD")
HOST = os.getenv("PERSISTENT_LOG_DB_HOST", "localhost")
PORT = os.getenv("PERSISTENT_LOG_DB_PORT", "5432")
URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/persistent_log"

engine = create_engine(URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
