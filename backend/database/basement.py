from typing import List, Optional
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TIMESTAMP

from . import Base

# Package B - Basement raft and perimeter walls
class Basement(Base):
    __tablename__ = "basement_fbg"

    timestamp = Column(TIMESTAMP, primary_key=True)

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
