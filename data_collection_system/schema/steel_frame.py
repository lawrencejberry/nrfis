from sqlalchemy import Column, String
from sqlalchemy.types import Time
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from . import Base

# Package D - Steel frame
class SteelFrame(Base):
    __tablename__ = "steel_frame_fbg"

    time = Column(Time, primary_key=True)

    # Section 1  N.B. measurements stored seperately to avoid ARRAY memory overhead
    L1 = Column(DOUBLE_PRECISION)
    L2 = Column(DOUBLE_PRECISION)
    L3 = Column(DOUBLE_PRECISION)
    L4 = Column(DOUBLE_PRECISION)
    L5 = Column(DOUBLE_PRECISION)
    L6 = Column(DOUBLE_PRECISION)
    L7 = Column(DOUBLE_PRECISION)
    L8 = Column(DOUBLE_PRECISION)
    L9 = Column(DOUBLE_PRECISION)
    L10 = Column(DOUBLE_PRECISION)
    L11 = Column(DOUBLE_PRECISION)
    L12 = Column(DOUBLE_PRECISION)
    L13 = Column(DOUBLE_PRECISION)
    L14 = Column(DOUBLE_PRECISION)
    L15 = Column(DOUBLE_PRECISION)
    L16 = Column(DOUBLE_PRECISION)
    L17 = Column(DOUBLE_PRECISION)
    L18 = Column(DOUBLE_PRECISION)

    # Section 2
    M1 = Column(DOUBLE_PRECISION)
    M2 = Column(DOUBLE_PRECISION)
    M3 = Column(DOUBLE_PRECISION)
    M4 = Column(DOUBLE_PRECISION)
    M5 = Column(DOUBLE_PRECISION)
    M6 = Column(DOUBLE_PRECISION)
    M7 = Column(DOUBLE_PRECISION)
    M8 = Column(DOUBLE_PRECISION)
    M9 = Column(DOUBLE_PRECISION)
    M10 = Column(DOUBLE_PRECISION)
    M11 = Column(DOUBLE_PRECISION)
    M12 = Column(DOUBLE_PRECISION)
    M13 = Column(DOUBLE_PRECISION)
    M14 = Column(DOUBLE_PRECISION)
    M15 = Column(DOUBLE_PRECISION)
    M16 = Column(DOUBLE_PRECISION)
    M17 = Column(DOUBLE_PRECISION)
    M18 = Column(DOUBLE_PRECISION)

    # Section 3a
    N1 = Column(DOUBLE_PRECISION)
    N2 = Column(DOUBLE_PRECISION)
    N3 = Column(DOUBLE_PRECISION)
    N4 = Column(DOUBLE_PRECISION)
    N5 = Column(DOUBLE_PRECISION)
    N6 = Column(DOUBLE_PRECISION)
    N7 = Column(DOUBLE_PRECISION)
    N8 = Column(DOUBLE_PRECISION)
    N9 = Column(DOUBLE_PRECISION)

    # Section 3b
    O1 = Column(DOUBLE_PRECISION)
    O2 = Column(DOUBLE_PRECISION)
    O3 = Column(DOUBLE_PRECISION)
    O4 = Column(DOUBLE_PRECISION)
    O5 = Column(DOUBLE_PRECISION)
    O6 = Column(DOUBLE_PRECISION)
    O7 = Column(DOUBLE_PRECISION)
    O8 = Column(DOUBLE_PRECISION)
    O9 = Column(DOUBLE_PRECISION)

    # Section 4
    P1 = Column(DOUBLE_PRECISION)
    P2 = Column(DOUBLE_PRECISION)
    P3 = Column(DOUBLE_PRECISION)
    P4 = Column(DOUBLE_PRECISION)
    P5 = Column(DOUBLE_PRECISION)
    P6 = Column(DOUBLE_PRECISION)
    P7 = Column(DOUBLE_PRECISION)
    P8 = Column(DOUBLE_PRECISION)
    P9 = Column(DOUBLE_PRECISION)
    P10 = Column(DOUBLE_PRECISION)
    P11 = Column(DOUBLE_PRECISION)
    P12 = Column(DOUBLE_PRECISION)
