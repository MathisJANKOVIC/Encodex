from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

DRIVERS = "mysql+pymysql"

HOST = os.environ.get("DB_HOST", "localhost")
PORT = os.environ.get("DB_PORT", "3306")

USER = os.environ.get("DB_USER", "root")
PASSWORD = os.environ.get("DB_PASSWORD", "")

DATABASE = os.environ.get("DB_NAME", "encodex")

engine = create_engine(f"{DRIVERS}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
LocalSession = sessionmaker(bind=engine)