from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DRIVERS = "mysql+pymysql"
USER = "root"
PASSWORD = ""
HOST = "db"
PORT = "3306"
DATABASE = "encodex"

engine = create_engine(f"{DRIVERS}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
LocalSession = sessionmaker(bind=engine)