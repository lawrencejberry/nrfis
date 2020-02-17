import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models import Package, Packages

# Create database engine
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:fourth-year@127.0.0.1/nrfisdb",
)
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
