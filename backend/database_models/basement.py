from sqlalchemy import Column, Float, DateTime

from . import Base

# Package B - Basement raft and perimeter walls
class Basement(Base):
    __tablename__ = "basement_fbg"

    timestamp = Column(DateTime, primary_key=True)

    # BA-FBG-EW01bot-Str  N.B. measurements stored seperately to avoid ARRAY memory overhead
    A1 = Column(Float)
    A2 = Column(Float)
    A3 = Column(Float)
    A4 = Column(Float)
    A5 = Column(Float)
    A6 = Column(Float)
    A7 = Column(Float)
    A8 = Column(Float)
    A9 = Column(Float)
    A10 = Column(Float)
    A11 = Column(Float)
    A12 = Column(Float)
    A13 = Column(Float)
    A14 = Column(Float)
    A15 = Column(Float)
    A16 = Column(Float)
    A17 = Column(Float)
    A18 = Column(Float)
    A19 = Column(Float)
    A20 = Column(Float)

    # BA-FBG-EW01top-Str
    B1 = Column(Float)
    B2 = Column(Float)
    B3 = Column(Float)
    B4 = Column(Float)
    B5 = Column(Float)
    B6 = Column(Float)
    B7 = Column(Float)
    B8 = Column(Float)
    B9 = Column(Float)
    B10 = Column(Float)
    B11 = Column(Float)
    B12 = Column(Float)
    B13 = Column(Float)
    B14 = Column(Float)
    B15 = Column(Float)
    B16 = Column(Float)
    B17 = Column(Float)
    B18 = Column(Float)
    B19 = Column(Float)
    B20 = Column(Float)

    # BA-FBG-NS01bot-Str/Tmp
    C1 = Column(Float)
    C2 = Column(Float)
    C3 = Column(Float)
    C4 = Column(Float)
    C5 = Column(Float)
    C6 = Column(Float)
    C7 = Column(Float)
    C8 = Column(Float)
    C9 = Column(Float)
    C10 = Column(Float)
    C11 = Column(Float)
    C12 = Column(Float)
    C13 = Column(Float)
    C14 = Column(Float)
    C15 = Column(Float)
    C16 = Column(Float)
    C17 = Column(Float)
    C18 = Column(Float)
    C19 = Column(Float)
    C20 = Column(Float)

    # BA-FBG-NS01top-Str/Tmp
    D1 = Column(Float)
    D2 = Column(Float)
    D3 = Column(Float)
    D4 = Column(Float)
    D5 = Column(Float)
    D6 = Column(Float)
    D7 = Column(Float)
    D8 = Column(Float)
    D9 = Column(Float)
    D10 = Column(Float)
    D11 = Column(Float)
    D12 = Column(Float)
    D13 = Column(Float)
    D14 = Column(Float)
    D15 = Column(Float)
    D16 = Column(Float)
    D17 = Column(Float)
    D18 = Column(Float)
    D19 = Column(Float)
    D20 = Column(Float)

    # BA-FBG-WW01wal-Str/Tmp
    E1 = Column(Float)
    E2 = Column(Float)
    E3 = Column(Float)
    E4 = Column(Float)
    E5 = Column(Float)
    E6 = Column(Float)

    # BA-FBG-EE01wal-Str/Tmp
    F1 = Column(Float)
    F2 = Column(Float)
    F3 = Column(Float)
    F4 = Column(Float)
    F5 = Column(Float)
    F6 = Column(Float)

    # BA-FBG-WW01thk-Str/Tmp
    G1 = Column(Float)
    G2 = Column(Float)
    G3 = Column(Float)
    G4 = Column(Float)
    G5 = Column(Float)
    G6 = Column(Float)

    # BA-FBG-EE01thk-Str/Tmp
    H1 = Column(Float)
    H2 = Column(Float)
    H3 = Column(Float)
    H4 = Column(Float)
    H5 = Column(Float)
    H6 = Column(Float)

    # BA-FBG-SS01thk-Str/Tmp
    I1 = Column(Float)
    I2 = Column(Float)
    I3 = Column(Float)
    I4 = Column(Float)
    I5 = Column(Float)
    I6 = Column(Float)

    # BA-FBG-EW01top/bot-Tmp
    J1 = Column(Float)
    J2 = Column(Float)
    J3 = Column(Float)
    J4 = Column(Float)
