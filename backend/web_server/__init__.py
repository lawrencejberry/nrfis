from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models import (
    Basement,
    StrongFloor,
    SteelFrame,
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)

# Create database engine
DATABASE_URL = "postgresql+psycopg2://postgres:@host.docker.internal/timescaletest"
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
