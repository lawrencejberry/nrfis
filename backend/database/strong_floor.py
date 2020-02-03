from typing import List
from datetime import datetime

from sqlalchemy import Column, DateTime, Float

from . import Base

# Package C - Strong floor
class StrongFloor(Base):
    __tablename__ = "strong_floor_fbg"

    timestamp = Column(DateTime, primary_key=True)

    # SF-FBG-EW01bot-Str  N.B. measurements stored seperately to avoid ARRAY memory overhead
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

    # SF-FBG-EW01top-Str
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

    # SF-FBG-EW02bot-Str
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

    # SF-FBG-EW02top-Str
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

    # SF-FBG-EW03bot-Str
    E1 = Column(Float)
    E2 = Column(Float)
    E3 = Column(Float)
    E4 = Column(Float)
    E5 = Column(Float)
    E6 = Column(Float)
    E7 = Column(Float)
    E8 = Column(Float)
    E9 = Column(Float)
    E10 = Column(Float)
    E11 = Column(Float)
    E12 = Column(Float)
    E13 = Column(Float)
    E14 = Column(Float)
    E15 = Column(Float)
    E16 = Column(Float)
    E17 = Column(Float)
    E18 = Column(Float)
    E19 = Column(Float)
    E20 = Column(Float)

    # SF-FBG-EW03top-Str
    F1 = Column(Float)
    F2 = Column(Float)
    F3 = Column(Float)
    F4 = Column(Float)
    F5 = Column(Float)
    F6 = Column(Float)
    F7 = Column(Float)
    F8 = Column(Float)
    F9 = Column(Float)
    F10 = Column(Float)
    F11 = Column(Float)
    F12 = Column(Float)
    F13 = Column(Float)
    F14 = Column(Float)
    F15 = Column(Float)
    F16 = Column(Float)
    F17 = Column(Float)
    F18 = Column(Float)
    F19 = Column(Float)
    F20 = Column(Float)

    # SF-FBG-NS01bot/top-Str
    G1 = Column(Float)
    G2 = Column(Float)
    G3 = Column(Float)
    G4 = Column(Float)
    G5 = Column(Float)
    G6 = Column(Float)
    G7 = Column(Float)
    G8 = Column(Float)
    G9 = Column(Float)
    G12 = Column(Float)
    G13 = Column(Float)
    G14 = Column(Float)
    G15 = Column(Float)
    G16 = Column(Float)
    G17 = Column(Float)
    G18 = Column(Float)
    G19 = Column(Float)
    G20 = Column(Float)

    # SF-FBG-NS02bot/top-Str
    H1 = Column(Float)
    H2 = Column(Float)
    H3 = Column(Float)
    H4 = Column(Float)
    H5 = Column(Float)
    H6 = Column(Float)
    H7 = Column(Float)
    H8 = Column(Float)
    H9 = Column(Float)
    H12 = Column(Float)
    H13 = Column(Float)
    H14 = Column(Float)
    H15 = Column(Float)
    H16 = Column(Float)
    H17 = Column(Float)
    H18 = Column(Float)
    H19 = Column(Float)
    H20 = Column(Float)

    # SF-FBG-NS03bot/top-Str
    I1 = Column(Float)
    I2 = Column(Float)
    I3 = Column(Float)
    I4 = Column(Float)
    I5 = Column(Float)
    I6 = Column(Float)
    I7 = Column(Float)
    I8 = Column(Float)
    I9 = Column(Float)
    I12 = Column(Float)
    I13 = Column(Float)
    I14 = Column(Float)
    I15 = Column(Float)
    I16 = Column(Float)
    I17 = Column(Float)
    I18 = Column(Float)
    I19 = Column(Float)

    # SF-FBG-NS04bot/top-Str
    J1 = Column(Float)
    J2 = Column(Float)
    J3 = Column(Float)
    J4 = Column(Float)
    J5 = Column(Float)
    J6 = Column(Float)
    J7 = Column(Float)
    J8 = Column(Float)
    J9 = Column(Float)
    J12 = Column(Float)
    J13 = Column(Float)
    J14 = Column(Float)
    J15 = Column(Float)
    J16 = Column(Float)
    J17 = Column(Float)
    J18 = Column(Float)
    J19 = Column(Float)
    J20 = Column(Float)

    # SF-FBG-NS05bot/top-Str
    K1 = Column(Float)
    K2 = Column(Float)
    K3 = Column(Float)
    K4 = Column(Float)
    K5 = Column(Float)
    K6 = Column(Float)
    K7 = Column(Float)
    K8 = Column(Float)
    K9 = Column(Float)
    K12 = Column(Float)
    K13 = Column(Float)
    K14 = Column(Float)
    K15 = Column(Float)
    K16 = Column(Float)
    K17 = Column(Float)
    K18 = Column(Float)
    K19 = Column(Float)
    K20 = Column(Float)

    # SF-FBG-NS06bot/top-Str
    L1 = Column(Float)
    L2 = Column(Float)
    L3 = Column(Float)
    L4 = Column(Float)
    L5 = Column(Float)
    L6 = Column(Float)
    L7 = Column(Float)
    L8 = Column(Float)
    L9 = Column(Float)
    L12 = Column(Float)
    L13 = Column(Float)
    L14 = Column(Float)
    L15 = Column(Float)
    L16 = Column(Float)
    L17 = Column(Float)
    L18 = Column(Float)
    L19 = Column(Float)
    L20 = Column(Float)

    # SF-FBG-NS07bot/top-Str
    M1 = Column(Float)
    M2 = Column(Float)
    M3 = Column(Float)
    M4 = Column(Float)
    M5 = Column(Float)
    M6 = Column(Float)
    M7 = Column(Float)
    M8 = Column(Float)
    M9 = Column(Float)
    M12 = Column(Float)
    M13 = Column(Float)
    M14 = Column(Float)
    M15 = Column(Float)
    M16 = Column(Float)
    M17 = Column(Float)
    M18 = Column(Float)
    M19 = Column(Float)
    M20 = Column(Float)

    # SF-FBG-NS01bot/top-Tmp
    N1 = Column(Float)
    N2 = Column(Float)
    N3 = Column(Float)
    N4 = Column(Float)
    N5 = Column(Float)
    N6 = Column(Float)
    N7 = Column(Float)
    N8 = Column(Float)
    N9 = Column(Float)
    N12 = Column(Float)
    N13 = Column(Float)
    N14 = Column(Float)
    N15 = Column(Float)
    N16 = Column(Float)
    N17 = Column(Float)
    N18 = Column(Float)
    N19 = Column(Float)
    N20 = Column(Float)

    # SF-FBG-NS04bot/top-Tmp
    O1 = Column(Float)
    O2 = Column(Float)
    O3 = Column(Float)
    O4 = Column(Float)
    O5 = Column(Float)
    O6 = Column(Float)
    O7 = Column(Float)
    O8 = Column(Float)
    O9 = Column(Float)
    O12 = Column(Float)
    O13 = Column(Float)
    O14 = Column(Float)
    O15 = Column(Float)
    O16 = Column(Float)
    O17 = Column(Float)
    O18 = Column(Float)
    O19 = Column(Float)
    O20 = Column(Float)

    # SF-FBG-NS07bot/top-Tmp
    P1 = Column(Float)
    P2 = Column(Float)
    P3 = Column(Float)
    P4 = Column(Float)
    P5 = Column(Float)
    P6 = Column(Float)
    P7 = Column(Float)
    P8 = Column(Float)
    P9 = Column(Float)
    P12 = Column(Float)
    P13 = Column(Float)
    P14 = Column(Float)
    P15 = Column(Float)
    P16 = Column(Float)
    P17 = Column(Float)
    P18 = Column(Float)
    P19 = Column(Float)
    P20 = Column(Float)

    def __init__(self, timestamp: datetime, peaks: List[List[float]] = None, **kwargs):
        """Defines the mapping between the input peaks and the internal database representation."""

        self.timestamp = timestamp

        if peaks is None:
            super().__init__(**kwargs)

        else:
            # SF-FBG-EW01bot-Str
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

            # SF-FBG-EW01top-Str
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

            # SF-FBG-EW02bot-Str
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

            # SF-FBG-EW02top-Str
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

            # SF-FBG-EW03bot-Str
            self.E1 = peaks[4][0]
            self.E2 = peaks[4][1]
            self.E3 = peaks[4][2]
            self.E4 = peaks[4][3]
            self.E5 = peaks[4][4]
            self.E6 = peaks[4][5]
            self.E7 = peaks[4][6]
            self.E8 = peaks[4][7]
            self.E9 = peaks[4][8]
            self.E10 = peaks[4][9]
            self.E11 = peaks[4][10]
            self.E12 = peaks[4][11]
            self.E13 = peaks[4][12]
            self.E14 = peaks[4][13]
            self.E15 = peaks[4][14]
            self.E16 = peaks[4][15]
            self.E17 = peaks[4][16]
            self.E18 = peaks[4][17]
            self.E19 = peaks[4][18]
            self.E20 = peaks[4][19]

            # SF-FBG-EW03top-Str
            self.F1 = peaks[5][0]
            self.F2 = peaks[5][1]
            self.F3 = peaks[5][2]
            self.F4 = peaks[5][3]
            self.F5 = peaks[5][4]
            self.F6 = peaks[5][5]
            self.F7 = peaks[5][6]
            self.F8 = peaks[5][7]
            self.F9 = peaks[5][8]
            self.F10 = peaks[5][9]
            self.F11 = peaks[5][10]
            self.F12 = peaks[5][11]
            self.F13 = peaks[5][12]
            self.F14 = peaks[5][13]
            self.F15 = peaks[5][14]
            self.F16 = peaks[5][15]
            self.F17 = peaks[5][16]
            self.F18 = peaks[5][17]
            self.F19 = peaks[5][18]
            self.F20 = peaks[5][19]

            # SF-FBG-NS01bot/top-Str
            self.G1 = peaks[6][0]
            self.G2 = peaks[6][1]
            self.G3 = peaks[6][2]
            self.G4 = peaks[6][3]
            self.G5 = peaks[6][4]
            self.G6 = peaks[6][5]
            self.G7 = peaks[6][6]
            self.G8 = peaks[6][7]
            self.G9 = peaks[6][8]
            self.G12 = peaks[6][11]
            self.G13 = peaks[6][12]
            self.G14 = peaks[6][13]
            self.G15 = peaks[6][14]
            self.G16 = peaks[6][15]
            self.G17 = peaks[6][16]
            self.G18 = peaks[6][17]
            self.G19 = peaks[6][18]
            self.G20 = peaks[6][19]

            # SF-FBG-NS02bot/top-Str
            self.H1 = peaks[7][0]
            self.H2 = peaks[7][1]
            self.H3 = peaks[7][2]
            self.H4 = peaks[7][3]
            self.H5 = peaks[7][4]
            self.H6 = peaks[7][5]
            self.H7 = peaks[7][6]
            self.H8 = peaks[7][7]
            self.H9 = peaks[7][8]
            self.H12 = peaks[7][11]
            self.H13 = peaks[7][12]
            self.H14 = peaks[7][13]
            self.H15 = peaks[7][14]
            self.H16 = peaks[7][15]
            self.H17 = peaks[7][16]
            self.H18 = peaks[7][17]
            self.H19 = peaks[7][18]
            self.H20 = peaks[7][19]

            # SF-FBG-NS03bot/top-Str
            self.I1 = peaks[8][0]
            self.I2 = peaks[8][1]
            self.I3 = peaks[8][2]
            self.I4 = peaks[8][3]
            self.I5 = peaks[8][4]
            self.I6 = peaks[8][5]
            self.I7 = peaks[8][6]
            self.I8 = peaks[8][7]
            self.I9 = peaks[8][8]
            self.I12 = peaks[8][11]
            self.I13 = peaks[8][12]
            self.I14 = peaks[8][13]
            self.I15 = peaks[8][14]
            self.I16 = peaks[8][15]
            self.I17 = peaks[8][16]
            self.I18 = peaks[8][17]
            self.I19 = peaks[8][18]

            # SF-FBG-NS04bot/top-Str
            self.J1 = peaks[9][0]
            self.J2 = peaks[9][1]
            self.J3 = peaks[9][2]
            self.J4 = peaks[9][3]
            self.J5 = peaks[9][4]
            self.J6 = peaks[9][5]
            self.J7 = peaks[9][6]
            self.J8 = peaks[9][7]
            self.J9 = peaks[9][8]
            self.J12 = peaks[9][11]
            self.J13 = peaks[9][12]
            self.J14 = peaks[9][13]
            self.J15 = peaks[9][14]
            self.J16 = peaks[9][15]
            self.J17 = peaks[9][16]
            self.J18 = peaks[9][17]
            self.J19 = peaks[9][18]
            self.J20 = peaks[9][19]

            # SF-FBG-NS05bot/top-Str
            self.K1 = peaks[10][0]
            self.K2 = peaks[10][1]
            self.K3 = peaks[10][2]
            self.K4 = peaks[10][3]
            self.K5 = peaks[10][4]
            self.K6 = peaks[10][5]
            self.K7 = peaks[10][6]
            self.K8 = peaks[10][7]
            self.K9 = peaks[10][8]
            self.K12 = peaks[10][11]
            self.K13 = peaks[10][12]
            self.K14 = peaks[10][13]
            self.K15 = peaks[10][14]
            self.K16 = peaks[10][15]
            self.K17 = peaks[10][16]
            self.K18 = peaks[10][17]
            self.K19 = peaks[10][18]
            self.K20 = peaks[10][19]

            # SF-FBG-NS06bot/top-Str
            self.L1 = peaks[11][0]
            self.L2 = peaks[11][1]
            self.L3 = peaks[11][2]
            self.L4 = peaks[11][3]
            self.L5 = peaks[11][4]
            self.L6 = peaks[11][5]
            self.L7 = peaks[11][6]
            self.L8 = peaks[11][7]
            self.L9 = peaks[11][8]
            self.L12 = peaks[11][11]
            self.L13 = peaks[11][12]
            self.L14 = peaks[11][13]
            self.L15 = peaks[11][14]
            self.L16 = peaks[11][15]
            self.L17 = peaks[11][16]
            self.L18 = peaks[11][17]
            self.L19 = peaks[11][18]
            self.L20 = peaks[11][19]

            # SF-FBG-NS07bot/top-Str
            self.M1 = peaks[12][0]
            self.M2 = peaks[12][1]
            self.M3 = peaks[12][2]
            self.M4 = peaks[12][3]
            self.M5 = peaks[12][4]
            self.M6 = peaks[12][5]
            self.M7 = peaks[12][6]
            self.M8 = peaks[12][7]
            self.M9 = peaks[12][8]
            self.M12 = peaks[12][11]
            self.M13 = peaks[12][12]
            self.M14 = peaks[12][13]
            self.M15 = peaks[12][14]
            self.M16 = peaks[12][15]
            self.M17 = peaks[12][16]
            self.M18 = peaks[12][17]
            self.M19 = peaks[12][18]
            self.M20 = peaks[12][19]

            # SF-FBG-NS01bot/top-Tmp
            self.N1 = peaks[13][0]
            self.N2 = peaks[13][1]
            self.N3 = peaks[13][2]
            self.N4 = peaks[13][3]
            self.N5 = peaks[13][4]
            self.N6 = peaks[13][5]
            self.N7 = peaks[13][6]
            self.N8 = peaks[13][7]
            self.N9 = peaks[13][8]
            self.N12 = peaks[13][11]
            self.N13 = peaks[13][12]
            self.N14 = peaks[13][13]
            self.N15 = peaks[13][14]
            self.N16 = peaks[13][15]
            self.N17 = peaks[13][16]
            self.N18 = peaks[13][17]
            self.N19 = peaks[13][18]
            self.N20 = peaks[13][19]

            # SF-FBG-NS04bot/top-Tmp
            self.O1 = peaks[14][0]
            self.O2 = peaks[14][1]
            self.O3 = peaks[14][2]
            self.O4 = peaks[14][3]
            self.O5 = peaks[14][4]
            self.O6 = peaks[14][5]
            self.O7 = peaks[14][6]
            self.O8 = peaks[14][7]
            self.O9 = peaks[14][8]
            self.O12 = peaks[14][11]
            self.O13 = peaks[14][12]
            self.O14 = peaks[14][13]
            self.O15 = peaks[14][14]
            self.O16 = peaks[14][15]
            self.O17 = peaks[14][16]
            self.O18 = peaks[14][17]
            self.O19 = peaks[14][18]
            self.O20 = peaks[14][19]

            # SF-FBG-NS07bot/top-Tmp
            self.P1 = peaks[15][0]
            self.P2 = peaks[15][1]
            self.P3 = peaks[15][2]
            self.P4 = peaks[15][3]
            self.P5 = peaks[15][4]
            self.P6 = peaks[15][5]
            self.P7 = peaks[15][6]
            self.P8 = peaks[15][7]
            self.P9 = peaks[15][8]
            self.P12 = peaks[15][11]
            self.P13 = peaks[15][12]
            self.P14 = peaks[15][13]
            self.P15 = peaks[15][14]
            self.P16 = peaks[15][15]
            self.P17 = peaks[15][16]
            self.P18 = peaks[15][17]
            self.P19 = peaks[15][18]
            self.P20 = peaks[15][19]