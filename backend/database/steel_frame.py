from typing import List
from datetime import datetime

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

    def __init__(self, timestamp: datetime, peaks: List[List[float]] = None, **kwargs):
        """Defines the mapping between the input peaks and the internal database representation."""

        self.timestamp = timestamp

        if peaks is None:
            super().__init__(**kwargs)

        else:
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
