import sys
import os
import logging
import logging.handlers

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models import Base, Packages


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# Create logger
os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fileHandler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(ROOT_DIR, "logs/data_collection_system.log"), when="midnight", utc=True
)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


# Create database engine
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./backend/data_collection_system/tests/.test.db"
)
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
