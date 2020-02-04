from typing import List
from datetime import datetime

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

    def __init__(self, timestamp: datetime, peaks: List[List[float]] = None, **kwargs):
        """Defines the mapping between the input peaks and the internal database representation."""

        self.timestamp = timestamp

        if peaks is None:
            super().__init__(**kwargs)

        else:
            # BA-FBG-EW01bot-Str
            self.A1 = peaks[0][0]
            self.A2 = peaks[0][1]
            self.A3 = peaks[0][2]
            self.A4 = peaks[0][3]
            self.A5 = peaks[0][4]
            self.A6 = peaks[0][5]
            self.A7 = peaks[0][6]
            self.A8 = peaks[0][7]
            self.A9 = peaks[0][8]
            self.A10 = peaks[0][9]
            self.A11 = peaks[0][10]
            self.A12 = peaks[0][11]
            self.A13 = peaks[0][12]
            self.A14 = peaks[0][13]
            self.A15 = peaks[0][14]
            self.A16 = peaks[0][15]
            self.A17 = peaks[0][16]
            self.A18 = peaks[0][17]
            self.A19 = peaks[0][18]
            self.A20 = peaks[0][19]

            # BA-FBG-EW01top-Str
            self.B1 = peaks[1][0]
            self.B2 = peaks[1][1]
            self.B3 = peaks[1][2]
            self.B4 = peaks[1][3]
            self.B5 = peaks[1][4]
            self.B6 = peaks[1][5]
            self.B7 = peaks[1][6]
            self.B8 = peaks[1][7]
            self.B9 = peaks[1][8]
            self.B10 = peaks[1][9]
            self.B11 = peaks[1][10]
            self.B12 = peaks[1][11]
            self.B13 = peaks[1][12]
            self.B14 = peaks[1][13]
            self.B15 = peaks[1][14]
            self.B16 = peaks[1][15]
            self.B17 = peaks[1][16]
            self.B18 = peaks[1][17]
            self.B19 = peaks[1][18]
            self.B20 = peaks[1][19]

            # BA-FBG-NS01bot-Str/Tmp
            self.C1 = peaks[2][0]
            self.C2 = peaks[2][1]
            self.C3 = peaks[2][2]
            self.C4 = peaks[2][3]
            self.C5 = peaks[2][4]
            self.C6 = peaks[2][5]
            self.C7 = peaks[2][6]
            self.C8 = peaks[2][7]
            self.C9 = peaks[2][8]
            self.C10 = peaks[2][9]
            self.C11 = peaks[2][10]
            self.C12 = peaks[2][11]
            self.C13 = peaks[2][12]
            self.C14 = peaks[2][13]
            self.C15 = peaks[2][14]
            self.C16 = peaks[2][15]
            self.C17 = peaks[2][16]
            self.C18 = peaks[2][17]
            self.C19 = peaks[2][18]
            self.C20 = peaks[2][19]

            # BA-FBG-NS01top-Str/Tmp
            self.D1 = peaks[3][0]
            self.D2 = peaks[3][1]
            self.D3 = peaks[3][2]
            self.D4 = peaks[3][3]
            self.D5 = peaks[3][4]
            self.D6 = peaks[3][5]
            self.D7 = peaks[3][6]
            self.D8 = peaks[3][7]
            self.D9 = peaks[3][8]
            self.D10 = peaks[3][9]
            self.D11 = peaks[3][10]
            self.D12 = peaks[3][11]
            self.D13 = peaks[3][12]
            self.D14 = peaks[3][13]
            self.D15 = peaks[3][14]
            self.D16 = peaks[3][15]
            self.D17 = peaks[3][16]
            self.D18 = peaks[3][17]
            self.D19 = peaks[3][18]
            self.D20 = peaks[3][19]

            # BA-FBG-WW01wal-Str/Tmp
            self.E1 = peaks[4][0]
            self.E2 = peaks[4][1]
            self.E3 = peaks[4][2]
            self.E4 = peaks[4][3]
            self.E5 = peaks[4][4]
            self.E6 = peaks[4][5]

            # BA-FBG-EE01wal-Str/Tmp
            self.F1 = peaks[5][0]
            self.F2 = peaks[5][1]
            self.F3 = peaks[5][2]
            self.F4 = peaks[5][3]
            self.F5 = peaks[5][4]
            self.F6 = peaks[5][5]

            # BA-FBG-WW01thk-Str/Tmp
            self.G1 = peaks[6][0]
            self.G2 = peaks[6][1]
            self.G3 = peaks[6][2]
            self.G4 = peaks[6][3]
            self.G5 = peaks[6][4]
            self.G6 = peaks[6][5]

            # BA-FBG-EE01thk-Str/Tmp
            self.H1 = peaks[7][0]
            self.H2 = peaks[7][1]
            self.H3 = peaks[7][2]
            self.H4 = peaks[7][3]
            self.H5 = peaks[7][4]
            self.H6 = peaks[7][5]

            # BA-FBG-SS01thk-Str/Tmp
            self.I1 = peaks[8][0]
            self.I2 = peaks[8][1]
            self.I3 = peaks[8][2]
            self.I4 = peaks[8][3]
            self.I5 = peaks[8][4]
            self.I6 = peaks[8][5]

            # BA-FBG-EW01top/bot-Tmp
            self.J1 = peaks[9][0]
            self.J2 = peaks[9][1]
            self.J3 = peaks[9][2]
            self.J4 = peaks[9][3]
