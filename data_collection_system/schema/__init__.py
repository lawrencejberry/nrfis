from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .basement import Basement
from .strong_floor import StrongFloor
from .steel_frame import SteelFrame
