import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models import (
    Package,
    basement_package,
    strong_floor_package,
    steel_frame_package,
)

# Create database engine
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:fourth-year@127.0.0.1/nrfisdb",
)
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
