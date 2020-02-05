from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models import (
    Package,
    basement_package,
    strong_floor_package,
    steel_frame_package,
)

# Create database engine
DATABASE_URL = "postgresql+psycopg2://postgres:@host.docker.internal/timescaletest"
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
