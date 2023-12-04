from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DRIVERS = "mysql+pymysql"
USER = "root"
PASSWORD = ""
HOST = "database"
PORT = "3306"
DATABASE = "codex-api"

engine = create_engine(f"{DRIVERS}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
session = sessionmaker(bind=engine)