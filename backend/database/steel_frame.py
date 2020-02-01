from typing import List
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.types import Time
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from . import Base

# Package D - Steel frame
class SteelFrameSample(Base):
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

    def __init__(self, time: datetime, peaks: List[List[float]]):
        """Defines the mapping between the input peaks and the internal database representation."""

        self.time = time

        # Section 1
        self.L1 = peaks[11][0]
        self.L2 = peaks[11][1]
        self.L3 = peaks[11][2]
        self.L4 = peaks[11][3]
        self.L5 = peaks[11][4]
        self.L6 = peaks[11][5]
        self.L7 = peaks[11][6]
        self.L8 = peaks[11][7]
        self.L9 = peaks[11][8]
        self.L10 = peaks[11][9]
        self.L11 = peaks[11][10]
        self.L12 = peaks[11][11]
        self.L13 = peaks[11][12]
        self.L14 = peaks[11][13]
        self.L15 = peaks[11][14]
        self.L16 = peaks[11][15]
        self.L17 = peaks[11][16]
        self.L18 = peaks[11][17]

        # Section 2
        self.M1 = peaks[12][0]
        self.M2 = peaks[12][1]
        self.M3 = peaks[12][2]
        self.M4 = peaks[12][3]
        self.M5 = peaks[12][4]
        self.M6 = peaks[12][5]
        self.M7 = peaks[12][6]
        self.M8 = peaks[12][7]
        self.M9 = peaks[12][8]
        self.M10 = peaks[12][9]
        self.M11 = peaks[12][10]
        self.M12 = peaks[12][11]
        self.M13 = peaks[12][12]
        self.M14 = peaks[12][13]
        self.M15 = peaks[12][14]
        self.M16 = peaks[12][15]
        self.M17 = peaks[12][16]
        self.M18 = peaks[12][17]

        # Section 3a
        self.N1 = peaks[13][0]
        self.N2 = peaks[13][1]
        self.N3 = peaks[13][2]
        self.N4 = peaks[13][3]
        self.N5 = peaks[13][4]
        self.N6 = peaks[13][5]
        self.N7 = peaks[13][6]
        self.N8 = peaks[13][7]
        self.N9 = peaks[13][8]

        # Section 3b
        self.O1 = peaks[14][0]
        self.O2 = peaks[14][1]
        self.O3 = peaks[14][2]
        self.O4 = peaks[14][3]
        self.O5 = peaks[14][4]
        self.O6 = peaks[14][5]
        self.O7 = peaks[14][6]
        self.O8 = peaks[14][7]
        self.O9 = peaks[14][8]

        # Section 4
        self.P1 = peaks[15][0]
        self.P2 = peaks[15][1]
        self.P3 = peaks[15][2]
        self.P4 = peaks[15][3]
        self.P5 = peaks[15][4]
        self.P6 = peaks[15][5]
        self.P7 = peaks[15][6]
        self.P8 = peaks[15][7]
        self.P9 = peaks[15][8]
        self.P10 = peaks[15][9]
        self.P11 = peaks[15][10]
        self.P12 = peaks[15][11]
