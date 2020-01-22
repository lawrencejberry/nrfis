from sqlalchemy import Column, String
from sqlalchemy.types import Time
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from . import Base

# Package B - Basement raft and perimeter walls
class Basement(Base):
    __tablename__ = "basement_fbg"

    time = Column(Time, primary_key=True)

    # BA-FBG-EW01bot-Str  N.B. measurements stored seperately to avoid ARRAY memory overhead
    A1 = Column(DOUBLE_PRECISION)
    A2 = Column(DOUBLE_PRECISION)
    A3 = Column(DOUBLE_PRECISION)
    A4 = Column(DOUBLE_PRECISION)
    A5 = Column(DOUBLE_PRECISION)
    A6 = Column(DOUBLE_PRECISION)
    A7 = Column(DOUBLE_PRECISION)
    A8 = Column(DOUBLE_PRECISION)
    A9 = Column(DOUBLE_PRECISION)
    A10 = Column(DOUBLE_PRECISION)
    A11 = Column(DOUBLE_PRECISION)
    A12 = Column(DOUBLE_PRECISION)
    A13 = Column(DOUBLE_PRECISION)
    A14 = Column(DOUBLE_PRECISION)
    A15 = Column(DOUBLE_PRECISION)
    A16 = Column(DOUBLE_PRECISION)
    A17 = Column(DOUBLE_PRECISION)
    A18 = Column(DOUBLE_PRECISION)
    A19 = Column(DOUBLE_PRECISION)
    A20 = Column(DOUBLE_PRECISION)

    # BA-FBG-EW01top-Str
    B1 = Column(DOUBLE_PRECISION)
    B2 = Column(DOUBLE_PRECISION)
    B3 = Column(DOUBLE_PRECISION)
    B4 = Column(DOUBLE_PRECISION)
    B5 = Column(DOUBLE_PRECISION)
    B6 = Column(DOUBLE_PRECISION)
    B7 = Column(DOUBLE_PRECISION)
    B8 = Column(DOUBLE_PRECISION)
    B9 = Column(DOUBLE_PRECISION)
    B10 = Column(DOUBLE_PRECISION)
    B11 = Column(DOUBLE_PRECISION)
    B12 = Column(DOUBLE_PRECISION)
    B13 = Column(DOUBLE_PRECISION)
    B14 = Column(DOUBLE_PRECISION)
    B15 = Column(DOUBLE_PRECISION)
    B16 = Column(DOUBLE_PRECISION)
    B17 = Column(DOUBLE_PRECISION)
    B18 = Column(DOUBLE_PRECISION)
    B19 = Column(DOUBLE_PRECISION)
    B20 = Column(DOUBLE_PRECISION)

    # BA-FBG-NS01bot-Str/Tmp
    C1 = Column(DOUBLE_PRECISION)
    C2 = Column(DOUBLE_PRECISION)
    C3 = Column(DOUBLE_PRECISION)
    C4 = Column(DOUBLE_PRECISION)
    C5 = Column(DOUBLE_PRECISION)
    C6 = Column(DOUBLE_PRECISION)
    C7 = Column(DOUBLE_PRECISION)
    C8 = Column(DOUBLE_PRECISION)
    C9 = Column(DOUBLE_PRECISION)
    C10 = Column(DOUBLE_PRECISION)
    C11 = Column(DOUBLE_PRECISION)
    C12 = Column(DOUBLE_PRECISION)
    C13 = Column(DOUBLE_PRECISION)
    C14 = Column(DOUBLE_PRECISION)
    C15 = Column(DOUBLE_PRECISION)
    C16 = Column(DOUBLE_PRECISION)
    C17 = Column(DOUBLE_PRECISION)
    C18 = Column(DOUBLE_PRECISION)
    C19 = Column(DOUBLE_PRECISION)
    C20 = Column(DOUBLE_PRECISION)

    # BA-FBG-NS01top-Str/Tmp
    D1 = Column(DOUBLE_PRECISION)
    D2 = Column(DOUBLE_PRECISION)
    D3 = Column(DOUBLE_PRECISION)
    D4 = Column(DOUBLE_PRECISION)
    D5 = Column(DOUBLE_PRECISION)
    D6 = Column(DOUBLE_PRECISION)
    D7 = Column(DOUBLE_PRECISION)
    D8 = Column(DOUBLE_PRECISION)
    D9 = Column(DOUBLE_PRECISION)
    D10 = Column(DOUBLE_PRECISION)
    D11 = Column(DOUBLE_PRECISION)
    D12 = Column(DOUBLE_PRECISION)
    D13 = Column(DOUBLE_PRECISION)
    D14 = Column(DOUBLE_PRECISION)
    D15 = Column(DOUBLE_PRECISION)
    D16 = Column(DOUBLE_PRECISION)
    D17 = Column(DOUBLE_PRECISION)
    D18 = Column(DOUBLE_PRECISION)
    D19 = Column(DOUBLE_PRECISION)
    D20 = Column(DOUBLE_PRECISION)

    # BA-FBG-WW01wal-Str/Tmp
    E1 = Column(DOUBLE_PRECISION)
    E2 = Column(DOUBLE_PRECISION)
    E3 = Column(DOUBLE_PRECISION)
    E4 = Column(DOUBLE_PRECISION)
    E5 = Column(DOUBLE_PRECISION)
    E6 = Column(DOUBLE_PRECISION)

    # BA-FBG-EE01wal-Str/Tmp
    F1 = Column(DOUBLE_PRECISION)
    F2 = Column(DOUBLE_PRECISION)
    F3 = Column(DOUBLE_PRECISION)
    F4 = Column(DOUBLE_PRECISION)
    F5 = Column(DOUBLE_PRECISION)
    F6 = Column(DOUBLE_PRECISION)

    # BA-FBG-WW01thk-Str/Tmp
    G1 = Column(DOUBLE_PRECISION)
    G2 = Column(DOUBLE_PRECISION)
    G3 = Column(DOUBLE_PRECISION)
    G4 = Column(DOUBLE_PRECISION)
    G5 = Column(DOUBLE_PRECISION)
    G6 = Column(DOUBLE_PRECISION)

    # BA-FBG-EE01thk-Str/Tmp
    H1 = Column(DOUBLE_PRECISION)
    H2 = Column(DOUBLE_PRECISION)
    H3 = Column(DOUBLE_PRECISION)
    H4 = Column(DOUBLE_PRECISION)
    H5 = Column(DOUBLE_PRECISION)
    H6 = Column(DOUBLE_PRECISION)

    # BA-FBG-SS01thk-Str/Tmp
    I1 = Column(DOUBLE_PRECISION)
    I2 = Column(DOUBLE_PRECISION)
    I3 = Column(DOUBLE_PRECISION)
    I4 = Column(DOUBLE_PRECISION)
    I5 = Column(DOUBLE_PRECISION)
    I6 = Column(DOUBLE_PRECISION)

    # BA-FBG-EW01top/bot-Tmp
    J1 = Column(DOUBLE_PRECISION)
    J2 = Column(DOUBLE_PRECISION)
    J3 = Column(DOUBLE_PRECISION)
    J4 = Column(DOUBLE_PRECISION)
