import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models import Package, Packages


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create database engine
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./backend/web_server/tests/.test.db",
)
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
