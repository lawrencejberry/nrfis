from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

from .basement import Basement
from .strong_floor import StrongFloor
from .steel_frame import SteelFrame


# Create database engine
db = create_engine(
    "postgresql+psycopg2://postgres:@localhost/timescaletest", echo=False
)
Session = sessionmaker(db)
