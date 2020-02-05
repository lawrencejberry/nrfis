from sqlalchemy import Column, DateTime, Float

from . import Base

# Package D - Steel frame
class SteelFrame(Base):
    __tablename__ = "steel_frame_fbg"

    timestamp = Column(DateTime, primary_key=True)

    # Section 1  N.B. measurements stored seperately to avoid ARRAY memory overhead
    L1 = Column(Float)
    L2 = Column(Float)
    L3 = Column(Float)
    L4 = Column(Float)
    L5 = Column(Float)
    L6 = Column(Float)
    L7 = Column(Float)
    L8 = Column(Float)
    L9 = Column(Float)
    L10 = Column(Float)
    L11 = Column(Float)
    L12 = Column(Float)
    L13 = Column(Float)
    L14 = Column(Float)
    L15 = Column(Float)
    L16 = Column(Float)
    L17 = Column(Float)
    L18 = Column(Float)

    # Section 2
    M1 = Column(Float)
    M2 = Column(Float)
    M3 = Column(Float)
    M4 = Column(Float)
    M5 = Column(Float)
    M6 = Column(Float)
    M7 = Column(Float)
    M8 = Column(Float)
    M9 = Column(Float)
    M10 = Column(Float)
    M11 = Column(Float)
    M12 = Column(Float)
    M13 = Column(Float)
    M14 = Column(Float)
    M15 = Column(Float)
    M16 = Column(Float)
    M17 = Column(Float)
    M18 = Column(Float)

    # Section 3a
    N1 = Column(Float)
    N2 = Column(Float)
    N3 = Column(Float)
    N4 = Column(Float)
    N5 = Column(Float)
    N6 = Column(Float)
    N7 = Column(Float)
    N8 = Column(Float)
    N9 = Column(Float)

    # Section 3b
    O1 = Column(Float)
    O2 = Column(Float)
    O3 = Column(Float)
    O4 = Column(Float)
    O5 = Column(Float)
    O6 = Column(Float)
    O7 = Column(Float)
    O8 = Column(Float)
    O9 = Column(Float)

    # Section 4
    P1 = Column(Float)
    P2 = Column(Float)
    P3 = Column(Float)
    P4 = Column(Float)
    P5 = Column(Float)
    P6 = Column(Float)
    P7 = Column(Float)
    P8 = Column(Float)
    P9 = Column(Float)
    P10 = Column(Float)
    P11 = Column(Float)
    P12 = Column(Float)
