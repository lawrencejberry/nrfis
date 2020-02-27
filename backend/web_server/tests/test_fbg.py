import pytest


@pytest.mark.parametrize("package", ["basement", "strong-floor", "steel-frame"])
@pytest.mark.parametrize("data_type", ["raw", "str", "tmp"])
@pytest.mark.parametrize("media_type", ["application/json", "text/csv"])
def test_response_ok(client, package, data_type, media_type):
    response = client.get(
        f"/fbg/{package}/{data_type}/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": media_type},
    )
    assert response.status_code == 200


def test_get_basement_raw_data(client):
    response = client.get(
        "/fbg/basement/raw/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "A1": 125.5,
            "A2": 125.5,
            "A3": 125.5,
            "A4": 125.5,
            "A5": 125.5,
            "A6": 125.5,
            "A7": 125.5,
            "A8": 125.5,
            "A9": 125.5,
            "A10": 125.5,
            "A11": 125.5,
            "A12": 125.5,
            "A13": 125.5,
            "A14": 125.5,
            "A15": 125.5,
            "A16": 125.5,
            "A17": 125.5,
            "A18": 125.5,
            "A19": 125.5,
            "A20": 125.5,
            "B1": 125.5,
            "B2": 125.5,
            "B3": 125.5,
            "B4": 125.5,
            "B5": 125.5,
            "B6": 125.5,
            "B7": 125.5,
            "B8": 125.5,
            "B9": 125.5,
            "B10": 125.5,
            "B11": 125.5,
            "B12": 125.5,
            "B13": 125.5,
            "B14": 125.5,
            "B15": 125.5,
            "B16": 125.5,
            "B17": 125.5,
            "B18": 125.5,
            "B19": 125.5,
            "B20": 125.5,
            "C1": 125.5,
            "C2": 125.5,
            "C3": 125.5,
            "C4": 125.5,
            "C5": 125.5,
            "C6": 125.5,
            "C7": 125.5,
            "C8": 125.5,
            "C9": 125.5,
            "C10": 125.5,
            "C11": 125.5,
            "C12": 125.5,
            "C13": 125.5,
            "C14": 125.5,
            "C15": 125.5,
            "C16": 125.5,
            "C17": 125.5,
            "C18": 125.5,
            "C19": 125.5,
            "C20": 125.5,
            "D1": 125.5,
            "D2": 125.5,
            "D3": 125.5,
            "D4": 125.5,
            "D5": 125.5,
            "D6": 125.5,
            "D7": 125.5,
            "D8": 125.5,
            "D9": 125.5,
            "D10": 125.5,
            "D11": 125.5,
            "D12": 125.5,
            "D13": 125.5,
            "D14": 125.5,
            "D15": 125.5,
            "D16": 125.5,
            "D17": 125.5,
            "D18": 125.5,
            "D19": 125.5,
            "D20": 125.5,
            "E1": 125.5,
            "E2": 125.5,
            "E3": 125.5,
            "E4": 125.5,
            "E5": 125.5,
            "E6": 125.5,
            "F1": 125.5,
            "F2": 125.5,
            "F3": 125.5,
            "F4": 125.5,
            "F5": 125.5,
            "F6": 125.5,
            "G1": 125.5,
            "G2": 125.5,
            "G3": 125.5,
            "G4": 125.5,
            "G5": 125.5,
            "G6": 125.5,
            "H1": 125.5,
            "H2": 125.5,
            "H3": 125.5,
            "H4": 125.5,
            "H5": 125.5,
            "H6": 125.5,
            "I1": 125.5,
            "I2": 125.5,
            "I3": 125.5,
            "I4": 125.5,
            "I5": 125.5,
            "I6": 125.5,
            "J1": 125.5,
            "J2": 125.5,
            "J3": 125.5,
            "J4": 125.5,
        }
    ]


def test_get_basement_strain_data(client):
    response = client.get(
        "/fbg/basement/str/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "BA_FBG_EW01_Str_bot01": 0,
            "BA_FBG_EW01_Str_bot02": 0,
            "BA_FBG_EW01_Str_bot03": 0,
            "BA_FBG_EW01_Str_bot04": 0,
            "BA_FBG_EW01_Str_bot05": 0,
            "BA_FBG_EW01_Str_bot06": 0,
            "BA_FBG_EW01_Str_bot07": 0,
            "BA_FBG_EW01_Str_bot08": 0,
            "BA_FBG_EW01_Str_bot09": 0,
            "BA_FBG_EW01_Str_bot10": 0,
            "BA_FBG_EW01_Str_bot11": 0,
            "BA_FBG_EW01_Str_bot12": 0,
            "BA_FBG_EW01_Str_bot13": 0,
            "BA_FBG_EW01_Str_bot14": 0,
            "BA_FBG_EW01_Str_bot15": 0,
            "BA_FBG_EW01_Str_bot16": 0,
            "BA_FBG_EW01_Str_bot17": 0,
            "BA_FBG_EW01_Str_bot18": 0,
            "BA_FBG_EW01_Str_bot19": 0,
            "BA_FBG_EW01_Str_bot20": 0,
            "BA_FBG_EW01_Str_top01": 0,
            "BA_FBG_EW01_Str_top02": 0,
            "BA_FBG_EW01_Str_top03": 0,
            "BA_FBG_EW01_Str_top04": 0,
            "BA_FBG_EW01_Str_top05": 0,
            "BA_FBG_EW01_Str_top06": 0,
            "BA_FBG_EW01_Str_top07": 0,
            "BA_FBG_EW01_Str_top08": 0,
            "BA_FBG_EW01_Str_top09": 0,
            "BA_FBG_EW01_Str_top10": 0,
            "BA_FBG_EW01_Str_top11": 0,
            "BA_FBG_EW01_Str_top12": 0,
            "BA_FBG_EW01_Str_top13": 0,
            "BA_FBG_EW01_Str_top14": 0,
            "BA_FBG_EW01_Str_top15": 0,
            "BA_FBG_EW01_Str_top16": 0,
            "BA_FBG_EW01_Str_top17": 0,
            "BA_FBG_EW01_Str_top18": 0,
            "BA_FBG_EW01_Str_top19": 0,
            "BA_FBG_EW01_Str_top20": 0,
            "BA_FBG_NS01_Str_bot14": 0,
            "BA_FBG_NS01_Str_bot13": 0,
            "BA_FBG_NS01_Str_bot12": 0,
            "BA_FBG_NS01_Str_bot11": 0,
            "BA_FBG_NS01_Str_bot10": 0,
            "BA_FBG_NS01_Str_bot9": 0,
            "BA_FBG_NS01_Str_bot8": 0,
            "BA_FBG_NS01_Str_bot7": 0,
            "BA_FBG_NS01_Str_bot6": 0,
            "BA_FBG_NS01_Str_bot5": 0,
            "BA_FBG_NS01_Str_bot4": 0,
            "BA_FBG_NS01_Str_bot3": 0,
            "BA_FBG_NS01_Str_bot2": 0,
            "BA_FBG_NS01_Str_bot1": 0,
            "BA_FBG_NN01_Str_wal01": 0,
            "BA_FBG_NN01_Str_wal02": 0,
            "BA_FBG_NN01_Str_wal04": 0,
            "BA_FBG_NN01_Str_wal03": 0,
            "BA_FBG_NS01_Str_top14": 0,
            "BA_FBG_NS01_Str_top13": 0,
            "BA_FBG_NS01_Str_top12": 0,
            "BA_FBG_NS01_Str_top11": 0,
            "BA_FBG_NS01_Str_top10": 0,
            "BA_FBG_NS01_Str_top9": 0,
            "BA_FBG_NS01_Str_top8": 0,
            "BA_FBG_NS01_Str_top7": 0,
            "BA_FBG_NS01_Str_top6": 0,
            "BA_FBG_NS01_Str_top5": 0,
            "BA_FBG_NS01_Str_top4": 0,
            "BA_FBG_NS01_Str_top3": 0,
            "BA_FBG_NS01_Str_top2": 0,
            "BA_FBG_NS01_Str_top1": 0,
            "BA_FBG_WW01_Str_wal01": 0,
            "BA_FBG_WW01_Str_wal02": 0,
            "BA_FBG_WW01_Str_wal04": 0,
            "BA_FBG_WW01_Str_wal03": 0,
            "BA_FBG_EE01_Str_wal01": 0,
            "BA_FBG_EE01_Str_wal02": 0,
            "BA_FBG_EE01_Str_wal04": 0,
            "BA_FBG_EE01_Str_wal03": 0,
            "BA_FBG_WW01_Str_thk01": 0,
            "BA_FBG_WW01_Str_thk02": 0,
            "BA_FBG_WW01_Str_thk04": 0,
            "BA_FBG_WW01_Str_thk03": 0,
            "BA_FBG_EE01_Str_thk01": 0,
            "BA_FBG_EE01_Str_thk02": 0,
            "BA_FBG_EE01_Str_thk04": 0,
            "BA_FBG_EE01_Str_thk03": 0,
            "BA_FBG_SS01_Str_thk01": 0,
            "BA_FBG_SS01_Str_thk02": 0,
            "BA_FBG_SS01_Str_thk04": 0,
            "BA_FBG_SS01_Str_thk03": 0,
        }
    ]


def test_get_basement_temperature_data(client):
    response = client.get(
        "/fbg/basement/tmp/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "BA_FBG_NN01_Tmp_wal05": 126.5,
            "BA_FBG_NN01_Tmp_wal06": 126.5,
            "BA_FBG_SS01_Tmp_wal06": 126.5,
            "BA_FBG_SS01_Tmp_wal05": 126.5,
            "BA_FBG_SS01_Tmp_wal03": 126.5,
            "BA_FBG_SS01_Tmp_wal04": 126.5,
            "BA_FBG_SS01_Tmp_wal02": 126.5,
            "BA_FBG_SS01_Tmp_wal01": 126.5,
            "BA_FBG_WW01_Tmp_wal05": 126.5,
            "BA_FBG_WW01_Tmp_wal06": 126.5,
            "BA_FBG_EE01_Tmp_wal05": 126.5,
            "BA_FBG_EE01_Tmp_wal06": 126.5,
            "BA_FBG_WW01_Tmp_thk05": 126.5,
            "BA_FBG_WW01_Tmp_thk06": 126.5,
            "BA_FBG_EE01_Tmp_thk05": 126.5,
            "BA_FBG_EE01_Tmp_thk06": 126.5,
            "BA_FBG_SS01_Tmp_thk05": 126.5,
            "BA_FBG_SS01_Tmp_thk06": 126.5,
            "BA_FBG_EW01_Tmp_bot03": 126.5,
            "BA_FBG_EW01_Tmp_top01": 126.5,
            "BA_FBG_EW01_Tmp_top02": 126.5,
            "BA_FBG_EW01_Tmp_top03": 126.5,
        }
    ]


def test_get_strong_floor_raw_data(client):
    response = client.get(
        "/fbg/strong-floor/raw/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "A1": 125.5,
            "A2": 125.5,
            "A3": 125.5,
            "A4": 125.5,
            "A5": 125.5,
            "A6": 125.5,
            "A7": 125.5,
            "A8": 125.5,
            "A9": 125.5,
            "A10": 125.5,
            "A11": 125.5,
            "A12": 125.5,
            "A13": 125.5,
            "A14": 125.5,
            "A15": 125.5,
            "A16": 125.5,
            "A17": 125.5,
            "A18": 125.5,
            "A19": 125.5,
            "A20": 125.5,
            "B1": 125.5,
            "B2": 125.5,
            "B3": 125.5,
            "B4": 125.5,
            "B5": 125.5,
            "B6": 125.5,
            "B7": 125.5,
            "B8": 125.5,
            "B9": 125.5,
            "B10": 125.5,
            "B11": 125.5,
            "B12": 125.5,
            "B13": 125.5,
            "B14": 125.5,
            "B15": 125.5,
            "B16": 125.5,
            "B17": 125.5,
            "B18": 125.5,
            "B19": 125.5,
            "B20": 125.5,
            "C1": 125.5,
            "C2": 125.5,
            "C3": 125.5,
            "C4": 125.5,
            "C5": 125.5,
            "C6": 125.5,
            "C7": 125.5,
            "C8": 125.5,
            "C9": 125.5,
            "C10": 125.5,
            "C11": 125.5,
            "C12": 125.5,
            "C13": 125.5,
            "C14": 125.5,
            "C15": 125.5,
            "C16": 125.5,
            "C17": 125.5,
            "C18": 125.5,
            "C19": 125.5,
            "C20": 125.5,
            "D1": 125.5,
            "D2": 125.5,
            "D3": 125.5,
            "D4": 125.5,
            "D5": 125.5,
            "D6": 125.5,
            "D7": 125.5,
            "D8": 125.5,
            "D9": 125.5,
            "D10": 125.5,
            "D11": 125.5,
            "D12": 125.5,
            "D13": 125.5,
            "D14": 125.5,
            "D15": 125.5,
            "D16": 125.5,
            "D17": 125.5,
            "D18": 125.5,
            "D19": 125.5,
            "D20": 125.5,
            "E1": 125.5,
            "E2": 125.5,
            "E3": 125.5,
            "E4": 125.5,
            "E5": 125.5,
            "E6": 125.5,
            "E7": 125.5,
            "E8": 125.5,
            "E9": 125.5,
            "E10": 125.5,
            "E11": 125.5,
            "E12": 125.5,
            "E13": 125.5,
            "E14": 125.5,
            "E15": 125.5,
            "E16": 125.5,
            "E17": 125.5,
            "E18": 125.5,
            "E19": 125.5,
            "E20": 125.5,
            "F1": 125.5,
            "F2": 125.5,
            "F3": 125.5,
            "F4": 125.5,
            "F5": 125.5,
            "F6": 125.5,
            "F7": 125.5,
            "F8": 125.5,
            "F9": 125.5,
            "F10": 125.5,
            "F11": 125.5,
            "F12": 125.5,
            "F13": 125.5,
            "F14": 125.5,
            "F15": 125.5,
            "F16": 125.5,
            "F17": 125.5,
            "F18": 125.5,
            "F19": 125.5,
            "F20": 125.5,
            "G1": 125.5,
            "G2": 125.5,
            "G3": 125.5,
            "G4": 125.5,
            "G5": 125.5,
            "G6": 125.5,
            "G7": 125.5,
            "G8": 125.5,
            "G9": 125.5,
            "G12": 125.5,
            "G13": 125.5,
            "G14": 125.5,
            "G15": 125.5,
            "G16": 125.5,
            "G17": 125.5,
            "G18": 125.5,
            "G19": 125.5,
            "G20": 125.5,
            "H1": 125.5,
            "H2": 125.5,
            "H3": 125.5,
            "H4": 125.5,
            "H5": 125.5,
            "H6": 125.5,
            "H7": 125.5,
            "H8": 125.5,
            "H9": 125.5,
            "H12": 125.5,
            "H13": 125.5,
            "H14": 125.5,
            "H15": 125.5,
            "H16": 125.5,
            "H17": 125.5,
            "H18": 125.5,
            "H19": 125.5,
            "H20": 125.5,
            "I1": 125.5,
            "I2": 125.5,
            "I3": 125.5,
            "I4": 125.5,
            "I5": 125.5,
            "I6": 125.5,
            "I7": 125.5,
            "I8": 125.5,
            "I9": 125.5,
            "I12": 125.5,
            "I13": 125.5,
            "I14": 125.5,
            "I15": 125.5,
            "I16": 125.5,
            "I17": 125.5,
            "I18": 125.5,
            "I19": 125.5,
            "J1": 125.5,
            "J2": 125.5,
            "J3": 125.5,
            "J4": 125.5,
            "J5": 125.5,
            "J6": 125.5,
            "J7": 125.5,
            "J8": 125.5,
            "J9": 125.5,
            "J12": 125.5,
            "J13": 125.5,
            "J14": 125.5,
            "J15": 125.5,
            "J16": 125.5,
            "J17": 125.5,
            "J18": 125.5,
            "J19": 125.5,
            "J20": 125.5,
            "K1": 125.5,
            "K2": 125.5,
            "K3": 125.5,
            "K4": 125.5,
            "K5": 125.5,
            "K6": 125.5,
            "K7": 125.5,
            "K8": 125.5,
            "K9": 125.5,
            "K12": 125.5,
            "K13": 125.5,
            "K14": 125.5,
            "K15": 125.5,
            "K16": 125.5,
            "K17": 125.5,
            "K18": 125.5,
            "K19": 125.5,
            "K20": 125.5,
            "L1": 125.5,
            "L2": 125.5,
            "L3": 125.5,
            "L4": 125.5,
            "L5": 125.5,
            "L6": 125.5,
            "L7": 125.5,
            "L8": 125.5,
            "L9": 125.5,
            "L12": 125.5,
            "L13": 125.5,
            "L14": 125.5,
            "L15": 125.5,
            "L16": 125.5,
            "L17": 125.5,
            "L18": 125.5,
            "L19": 125.5,
            "L20": 125.5,
            "M1": 125.5,
            "M2": 125.5,
            "M3": 125.5,
            "M4": 125.5,
            "M5": 125.5,
            "M6": 125.5,
            "M7": 125.5,
            "M8": 125.5,
            "M9": 125.5,
            "M12": 125.5,
            "M13": 125.5,
            "M14": 125.5,
            "M15": 125.5,
            "M16": 125.5,
            "M17": 125.5,
            "M18": 125.5,
            "M19": 125.5,
            "M20": 125.5,
            "N1": 125.5,
            "N2": 125.5,
            "N3": 125.5,
            "N4": 125.5,
            "N5": 125.5,
            "N6": 125.5,
            "N7": 125.5,
            "N8": 125.5,
            "N9": 125.5,
            "N12": 125.5,
            "N13": 125.5,
            "N14": 125.5,
            "N15": 125.5,
            "N16": 125.5,
            "N17": 125.5,
            "N18": 125.5,
            "N19": 125.5,
            "N20": 125.5,
            "O1": 125.5,
            "O2": 125.5,
            "O3": 125.5,
            "O4": 125.5,
            "O5": 125.5,
            "O6": 125.5,
            "O7": 125.5,
            "O8": 125.5,
            "O9": 125.5,
            "O12": 125.5,
            "O13": 125.5,
            "O14": 125.5,
            "O15": 125.5,
            "O16": 125.5,
            "O17": 125.5,
            "O18": 125.5,
            "O19": 125.5,
            "O20": 125.5,
            "P1": 125.5,
            "P2": 125.5,
            "P3": 125.5,
            "P4": 125.5,
            "P5": 125.5,
            "P6": 125.5,
            "P7": 125.5,
            "P8": 125.5,
            "P9": 125.5,
            "P12": 125.5,
            "P13": 125.5,
            "P14": 125.5,
            "P15": 125.5,
            "P16": 125.5,
            "P17": 125.5,
            "P18": 125.5,
            "P19": 125.5,
            "P20": 125.5,
        }
    ]


def test_get_strong_floor_strain_data(client):
    response = client.get(
        "/fbg/strong-floor/str/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "SF_FBG_EW01_Str_bot01": 0,
            "SF_FBG_EW01_Str_bot02": 0,
            "SF_FBG_EW01_Str_bot03": 0,
            "SF_FBG_EW01_Str_bot04": 0,
            "SF_FBG_EW01_Str_bot05": 0,
            "SF_FBG_EW01_Str_bot06": 0,
            "SF_FBG_EW01_Str_bot07": 0,
            "SF_FBG_EW01_Str_bot08": 0,
            "SF_FBG_EW01_Str_bot09": 0,
            "SF_FBG_EW01_Str_bot10": 0,
            "SF_FBG_EW01_Str_bot11": 0,
            "SF_FBG_EW01_Str_bot12": 0,
            "SF_FBG_EW01_Str_bot13": 0,
            "SF_FBG_EW01_Str_bot14": 0,
            "SF_FBG_EW01_Str_bot15": 0,
            "SF_FBG_EW01_Str_bot16": 0,
            "SF_FBG_EW01_Str_bot17": 0,
            "SF_FBG_EW01_Str_bot18": 0,
            "SF_FBG_EW01_Str_bot19": 0,
            "SF_FBG_EW01_Str_bot20": 0,
            "SF_FBG_EW01_Str_top01": 0,
            "SF_FBG_EW01_Str_top02": 0,
            "SF_FBG_EW01_Str_top03": 0,
            "SF_FBG_EW01_Str_top04": 0,
            "SF_FBG_EW01_Str_top05": 0,
            "SF_FBG_EW01_Str_top06": 0,
            "SF_FBG_EW01_Str_top07": 0,
            "SF_FBG_EW01_Str_top08": 0,
            "SF_FBG_EW01_Str_top09": 0,
            "SF_FBG_EW01_Str_top10": 0,
            "SF_FBG_EW01_Str_top11": 0,
            "SF_FBG_EW01_Str_top12": 0,
            "SF_FBG_EW01_Str_top13": 0,
            "SF_FBG_EW01_Str_top14": 0,
            "SF_FBG_EW01_Str_top15": 0,
            "SF_FBG_EW01_Str_top16": 0,
            "SF_FBG_EW01_Str_top17": 0,
            "SF_FBG_EW01_Str_top18": 0,
            "SF_FBG_EW01_Str_top19": 0,
            "SF_FBG_EW01_Str_top20": 0,
            "SF_FBG_EW02_Str_bot01": 0,
            "SF_FBG_EW02_Str_bot02": 0,
            "SF_FBG_EW02_Str_bot03": 0,
            "SF_FBG_EW02_Str_bot04": 0,
            "SF_FBG_EW02_Str_bot05": 0,
            "SF_FBG_EW02_Str_bot06": 0,
            "SF_FBG_EW02_Str_bot07": 0,
            "SF_FBG_EW02_Str_bot08": 0,
            "SF_FBG_EW02_Str_bot09": 0,
            "SF_FBG_EW02_Str_bot10": 0,
            "SF_FBG_EW02_Str_bot11": 0,
            "SF_FBG_EW02_Str_bot12": 0,
            "SF_FBG_EW02_Str_bot13": 0,
            "SF_FBG_EW02_Str_bot14": 0,
            "SF_FBG_EW02_Str_bot15": 0,
            "SF_FBG_EW02_Str_bot16": 0,
            "SF_FBG_EW02_Str_bot17": 0,
            "SF_FBG_EW02_Str_bot18": 0,
            "SF_FBG_EW02_Str_bot19": 0,
            "SF_FBG_EW02_Str_bot20": 0,
            "SF_FBG_EW02_Str_top01": 0,
            "SF_FBG_EW02_Str_top02": 0,
            "SF_FBG_EW02_Str_top03": 0,
            "SF_FBG_EW02_Str_top04": 0,
            "SF_FBG_EW02_Str_top05": 0,
            "SF_FBG_EW02_Str_top06": 0,
            "SF_FBG_EW02_Str_top07": 0,
            "SF_FBG_EW02_Str_top08": 0,
            "SF_FBG_EW02_Str_top09": 0,
            "SF_FBG_EW02_Str_top10": 0,
            "SF_FBG_EW02_Str_top11": 0,
            "SF_FBG_EW02_Str_top12": 0,
            "SF_FBG_EW02_Str_top13": 0,
            "SF_FBG_EW02_Str_top14": 0,
            "SF_FBG_EW02_Str_top15": 0,
            "SF_FBG_EW02_Str_top16": 0,
            "SF_FBG_EW02_Str_top17": 0,
            "SF_FBG_EW02_Str_top18": 0,
            "SF_FBG_EW02_Str_top19": 0,
            "SF_FBG_EW02_Str_top20": 0,
            "SF_FBG_EW03_Str_bot01": 0,
            "SF_FBG_EW03_Str_bot02": 0,
            "SF_FBG_EW03_Str_bot03": 0,
            "SF_FBG_EW03_Str_bot04": 0,
            "SF_FBG_EW03_Str_bot05": 0,
            "SF_FBG_EW03_Str_bot06": 0,
            "SF_FBG_EW03_Str_bot07": 0,
            "SF_FBG_EW03_Str_bot08": 0,
            "SF_FBG_EW03_Str_bot09": 0,
            "SF_FBG_EW03_Str_bot10": 0,
            "SF_FBG_EW03_Str_bot11": 0,
            "SF_FBG_EW03_Str_bot12": 0,
            "SF_FBG_EW03_Str_bot13": 0,
            "SF_FBG_EW03_Str_bot14": 0,
            "SF_FBG_EW03_Str_bot15": 0,
            "SF_FBG_EW03_Str_bot16": 0,
            "SF_FBG_EW03_Str_bot17": 0,
            "SF_FBG_EW03_Str_bot18": 0,
            "SF_FBG_EW03_Str_bot19": 0,
            "SF_FBG_EW03_Str_bot20": 0,
            "SF_FBG_EW03_Str_top01": 0,
            "SF_FBG_EW03_Str_top02": 0,
            "SF_FBG_EW03_Str_top03": 0,
            "SF_FBG_EW03_Str_top04": 0,
            "SF_FBG_EW03_Str_top05": 0,
            "SF_FBG_EW03_Str_top06": 0,
            "SF_FBG_EW03_Str_top07": 0,
            "SF_FBG_EW03_Str_top08": 0,
            "SF_FBG_EW03_Str_top09": 0,
            "SF_FBG_EW03_Str_top10": 0,
            "SF_FBG_EW03_Str_top11": 0,
            "SF_FBG_EW03_Str_top12": 0,
            "SF_FBG_EW03_Str_top13": 0,
            "SF_FBG_EW03_Str_top14": 0,
            "SF_FBG_EW03_Str_top15": 0,
            "SF_FBG_EW03_Str_top16": 0,
            "SF_FBG_EW03_Str_top17": 0,
            "SF_FBG_EW03_Str_top18": 0,
            "SF_FBG_EW03_Str_top19": 0,
            "SF_FBG_EW03_Str_top20": 0,
            "SF_FBG_NS01_Str_bot01": 0,
            "SF_FBG_NS01_Str_bot02": 0,
            "SF_FBG_NS01_Str_bot03": 0,
            "SF_FBG_NS01_Str_bot04": 0,
            "SF_FBG_NS01_Str_bot05": 0,
            "SF_FBG_NS01_Str_bot06": 0,
            "SF_FBG_NS01_Str_bot07": 0,
            "SF_FBG_NS01_Str_bot08": 0,
            "SF_FBG_NS01_Str_bot09": 0,
            "SF_FBG_NS01_Str_top09": 0,
            "SF_FBG_NS01_Str_top08": 0,
            "SF_FBG_NS01_Str_top07": 0,
            "SF_FBG_NS01_Str_top06": 0,
            "SF_FBG_NS01_Str_top05": 0,
            "SF_FBG_NS01_Str_top04": 0,
            "SF_FBG_NS01_Str_top03": 0,
            "SF_FBG_NS01_Str_top02": 0,
            "SF_FBG_NS01_Str_top01": 0,
            "SF_FBG_NS02_Str_bot01": 0,
            "SF_FBG_NS02_Str_bot02": 0,
            "SF_FBG_NS02_Str_bot03": 0,
            "SF_FBG_NS02_Str_bot04": 0,
            "SF_FBG_NS02_Str_bot05": 0,
            "SF_FBG_NS02_Str_bot06": 0,
            "SF_FBG_NS02_Str_bot07": 0,
            "SF_FBG_NS02_Str_bot08": 0,
            "SF_FBG_NS02_Str_bot09": 0,
            "SF_FBG_NS02_Str_top09": 0,
            "SF_FBG_NS02_Str_top08": 0,
            "SF_FBG_NS02_Str_top07": 0,
            "SF_FBG_NS02_Str_top06": 0,
            "SF_FBG_NS02_Str_top05": 0,
            "SF_FBG_NS02_Str_top04": 0,
            "SF_FBG_NS02_Str_top03": 0,
            "SF_FBG_NS02_Str_top02": 0,
            "SF_FBG_NS02_Str_top01": 0,
            "SF_FBG_NS03_Str_bot01": 0,
            "SF_FBG_NS03_Str_bot02": 0,
            "SF_FBG_NS03_Str_bot03": 0,
            "SF_FBG_NS03_Str_bot04": 0,
            "SF_FBG_NS03_Str_bot05": 0,
            "SF_FBG_NS03_Str_bot06": 0,
            "SF_FBG_NS03_Str_bot07": 0,
            "SF_FBG_NS03_Str_bot08": 0,
            "SF_FBG_NS03_Str_bot09": 0,
            "SF_FBG_NS03_Str_top09": 0,
            "SF_FBG_NS03_Str_top08": 0,
            "SF_FBG_NS03_Str_top06": 0,
            "SF_FBG_NS03_Str_top05": 0,
            "SF_FBG_NS03_Str_top04": 0,
            "SF_FBG_NS03_Str_top03": 0,
            "SF_FBG_NS03_Str_top02": 0,
            "SF_FBG_NS03_Str_top01": 0,
            "SF_FBG_NS04_Str_bot01": 0,
            "SF_FBG_NS04_Str_bot02": 0,
            "SF_FBG_NS04_Str_bot03": 0,
            "SF_FBG_NS04_Str_bot04": 0,
            "SF_FBG_NS04_Str_bot05": 0,
            "SF_FBG_NS04_Str_bot06": 0,
            "SF_FBG_NS04_Str_bot07": 0,
            "SF_FBG_NS04_Str_bot08": 0,
            "SF_FBG_NS04_Str_bot09": 0,
            "SF_FBG_NS04_Str_top09": 0,
            "SF_FBG_NS04_Str_top08": 0,
            "SF_FBG_NS04_Str_top07": 0,
            "SF_FBG_NS04_Str_top06": 0,
            "SF_FBG_NS04_Str_top05": 0,
            "SF_FBG_NS04_Str_top04": 0,
            "SF_FBG_NS04_Str_top03": 0,
            "SF_FBG_NS04_Str_top02": 0,
            "SF_FBG_NS04_Str_top01": 0,
            "SF_FBG_NS05_Str_bot01": 0,
            "SF_FBG_NS05_Str_bot02": 0,
            "SF_FBG_NS05_Str_bot03": 0,
            "SF_FBG_NS05_Str_bot04": 0,
            "SF_FBG_NS05_Str_bot05": 0,
            "SF_FBG_NS05_Str_bot06": 0,
            "SF_FBG_NS05_Str_bot07": 0,
            "SF_FBG_NS05_Str_bot08": 0,
            "SF_FBG_NS05_Str_bot09": 0,
            "SF_FBG_NS05_Str_top09": 0,
            "SF_FBG_NS05_Str_top08": 0,
            "SF_FBG_NS05_Str_top07": 0,
            "SF_FBG_NS05_Str_top06": 0,
            "SF_FBG_NS05_Str_top05": 0,
            "SF_FBG_NS05_Str_top04": 0,
            "SF_FBG_NS05_Str_top03": 0,
            "SF_FBG_NS05_Str_top02": 0,
            "SF_FBG_NS05_Str_top01": 0,
            "SF_FBG_NS06_Str_bot01": 0,
            "SF_FBG_NS06_Str_bot02": 0,
            "SF_FBG_NS06_Str_bot03": 0,
            "SF_FBG_NS06_Str_bot04": 0,
            "SF_FBG_NS06_Str_bot05": 0,
            "SF_FBG_NS06_Str_bot06": 0,
            "SF_FBG_NS06_Str_bot07": 0,
            "SF_FBG_NS06_Str_bot08": 0,
            "SF_FBG_NS06_Str_bot09": 0,
            "SF_FBG_NS06_Str_top09": 0,
            "SF_FBG_NS06_Str_top08": 0,
            "SF_FBG_NS06_Str_top07": 0,
            "SF_FBG_NS06_Str_top06": 0,
            "SF_FBG_NS06_Str_top05": 0,
            "SF_FBG_NS06_Str_top04": 0,
            "SF_FBG_NS06_Str_top03": 0,
            "SF_FBG_NS06_Str_top02": 0,
            "SF_FBG_NS06_Str_top01": 0,
            "SF_FBG_NS07_Str_bot01": 0,
            "SF_FBG_NS07_Str_bot02": 0,
            "SF_FBG_NS07_Str_bot03": 0,
            "SF_FBG_NS07_Str_bot04": 0,
            "SF_FBG_NS07_Str_bot05": 0,
            "SF_FBG_NS07_Str_bot06": 0,
            "SF_FBG_NS07_Str_bot07": 0,
            "SF_FBG_NS07_Str_bot08": 0,
            "SF_FBG_NS07_Str_bot09": 0,
            "SF_FBG_NS07_Str_top09": 0,
            "SF_FBG_NS07_Str_top08": 0,
            "SF_FBG_NS07_Str_top07": 0,
            "SF_FBG_NS07_Str_top06": 0,
            "SF_FBG_NS07_Str_top05": 0,
            "SF_FBG_NS07_Str_top04": 0,
            "SF_FBG_NS07_Str_top03": 0,
            "SF_FBG_NS07_Str_top02": 0,
            "SF_FBG_NS07_Str_top01": 0,
        }
    ]


def test_get_strong_floor_temperature_data(client):
    response = client.get(
        "/fbg/strong-floor/tmp/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "SF_FBG_NS01_Tmp_bot01": 126.5,
            "SF_FBG_NS01_Tmp_bot02": 126.5,
            "SF_FBG_NS01_Tmp_bot03": 126.5,
            "SF_FBG_NS01_Tmp_bot04": 126.5,
            "SF_FBG_NS01_Tmp_bot05": 126.5,
            "SF_FBG_NS01_Tmp_bot06": 126.5,
            "SF_FBG_NS01_Tmp_bot07": 126.5,
            "SF_FBG_NS01_Tmp_bot08": 126.5,
            "SF_FBG_NS01_Tmp_bot09": 126.5,
            "SF_FBG_NS01_Tmp_top09": 126.5,
            "SF_FBG_NS01_Tmp_top08": 126.5,
            "SF_FBG_NS01_Tmp_top07": 126.5,
            "SF_FBG_NS01_Tmp_top06": 126.5,
            "SF_FBG_NS01_Tmp_top05": 126.5,
            "SF_FBG_NS01_Tmp_top04": 126.5,
            "SF_FBG_NS01_Tmp_top03": 126.5,
            "SF_FBG_NS01_Tmp_top02": 126.5,
            "SF_FBG_NS01_Tmp_top01": 126.5,
            "SF_FBG_NS04_Tmp_bot01": 126.5,
            "SF_FBG_NS04_Tmp_bot02": 126.5,
            "SF_FBG_NS04_Tmp_bot03": 126.5,
            "SF_FBG_NS04_Tmp_bot04": 126.5,
            "SF_FBG_NS04_Tmp_bot05": 126.5,
            "SF_FBG_NS04_Tmp_bot06": 126.5,
            "SF_FBG_NS04_Tmp_bot07": 126.5,
            "SF_FBG_NS04_Tmp_bot08": 126.5,
            "SF_FBG_NS04_Tmp_bot09": 126.5,
            "SF_FBG_NS04_Tmp_top09": 126.5,
            "SF_FBG_NS04_Tmp_top08": 126.5,
            "SF_FBG_NS04_Tmp_top07": 126.5,
            "SF_FBG_NS04_Tmp_top06": 126.5,
            "SF_FBG_NS04_Tmp_top05": 126.5,
            "SF_FBG_NS04_Tmp_top04": 126.5,
            "SF_FBG_NS04_Tmp_top03": 126.5,
            "SF_FBG_NS04_Tmp_top02": 126.5,
            "SF_FBG_NS04_Tmp_top01": 126.5,
            "SF_FBG_NS07_Tmp_bot01": 126.5,
            "SF_FBG_NS07_Tmp_bot02": 126.5,
            "SF_FBG_NS07_Tmp_bot03": 126.5,
            "SF_FBG_NS07_Tmp_bot04": 126.5,
            "SF_FBG_NS07_Tmp_bot05": 126.5,
            "SF_FBG_NS07_Tmp_bot06": 126.5,
            "SF_FBG_NS07_Tmp_bot07": 126.5,
            "SF_FBG_NS07_Tmp_bot08": 126.5,
            "SF_FBG_NS07_Tmp_bot09": 126.5,
            "SF_FBG_NS07_Tmp_top09": 126.5,
            "SF_FBG_NS07_Tmp_top08": 126.5,
            "SF_FBG_NS07_Tmp_top07": 126.5,
            "SF_FBG_NS07_Tmp_top06": 126.5,
            "SF_FBG_NS07_Tmp_top05": 126.5,
            "SF_FBG_NS07_Tmp_top04": 126.5,
            "SF_FBG_NS07_Tmp_top03": 126.5,
            "SF_FBG_NS07_Tmp_top02": 126.5,
            "SF_FBG_NS07_Tmp_top01": 126.5,
        }
    ]


def test_get_steel_frame_raw_data(client):
    response = client.get(
        "/fbg/steel-frame/raw/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "L1": 125.5,
            "L2": 125.5,
            "L3": 125.5,
            "L4": 125.5,
            "L5": 125.5,
            "L6": 125.5,
            "L7": 125.5,
            "L8": 125.5,
            "L9": 125.5,
            "L10": 125.5,
            "L11": 125.5,
            "L12": 125.5,
            "L13": 125.5,
            "L14": 125.5,
            "L15": 125.5,
            "L16": 125.5,
            "L17": 125.5,
            "L18": 125.5,
            "M1": 125.5,
            "M2": 125.5,
            "M3": 125.5,
            "M4": 125.5,
            "M5": 125.5,
            "M6": 125.5,
            "M7": 125.5,
            "M8": 125.5,
            "M9": 125.5,
            "M10": 125.5,
            "M11": 125.5,
            "M12": 125.5,
            "M13": 125.5,
            "M14": 125.5,
            "M15": 125.5,
            "M16": 125.5,
            "M17": 125.5,
            "M18": 125.5,
            "N1": 125.5,
            "N2": 125.5,
            "N3": 125.5,
            "N4": 125.5,
            "N5": 125.5,
            "N6": 125.5,
            "N7": 125.5,
            "N8": 125.5,
            "N9": 125.5,
            "O1": 125.5,
            "O2": 125.5,
            "O3": 125.5,
            "O4": 125.5,
            "O5": 125.5,
            "O6": 125.5,
            "O7": 125.5,
            "O8": 125.5,
            "O9": 125.5,
            "P1": 125.5,
            "P2": 125.5,
            "P3": 125.5,
            "P4": 125.5,
            "P5": 125.5,
            "P6": 125.5,
            "P7": 125.5,
            "P8": 125.5,
            "P9": 125.5,
            "P10": 125.5,
            "P11": 125.5,
            "P12": 125.5,
        }
    ]


def test_get_steel_frame_strain_data(client):
    response = client.get(
        "/fbg/steel-frame/str/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "FR_FBG_CL_D1_0a": -126500000,
            "FR_FBG_CL_D1_0b": -126500000,
            "FR_FBG_CL_D1_1a": -126500000,
            "FR_FBG_CL_D1_1b": -126500000,
            "FR_FBG_CL_D1_2a": -126500000,
            "FR_FBG_CL_D1_2b": -126500000,
            "FR_FBG_BM_D13_1a": -126500000,
            "FR_FBG_BM_D13_2a": -126500000,
            "FR_FBG_BM_D13_3a": -126500000,
            "FR_FBG_BM_D13_1b": -126500000,
            "FR_FBG_BM_D13_2b": -126500000,
            "FR_FBG_BM_D13_3b": -126500000,
            "FR_FBG_CL_D3_0a": -126500000,
            "FR_FBG_CL_D3_0b": -126500000,
            "FR_FBG_CL_D3_1a": -126500000,
            "FR_FBG_CL_D3_1b": -126500000,
            "FR_FBG_CL_D3_2a": -126500000,
            "FR_FBG_CL_D3_2b": -126500000,
            "FR_FBG_BM_D34_1a": -126500000,
            "FR_FBG_BM_D34_2a": -126500000,
            "FR_FBG_BM_D34_3a": -126500000,
            "FR_FBG_BM_D34_1b": -126500000,
            "FR_FBG_BM_D34_2b": -126500000,
            "FR_FBG_BM_D34_3b": -126500000,
            "FR_FBG_CL_D4_0a": -126500000,
            "FR_FBG_CL_D4_0b": -126500000,
            "FR_FBG_CL_D4_1a": -126500000,
            "FR_FBG_CL_D4_1b": -126500000,
            "FR_FBG_BM_D46_1a": -126500000,
            "FR_FBG_BM_D46_1b": -126500000,
            "FR_FBG_CL_D4_2a": -126500000,
            "FR_FBG_CL_D4_2b": -126500000,
            "FR_FBG_BM_D46_2a": -126500000,
            "FR_FBG_BM_D46_3a": -126500000,
            "FR_FBG_BM_D46_2b": -126500000,
            "FR_FBG_BM_D46_3b": -126500000,
            "FR_FBG_CL_D6_0a": -126500000,
            "FR_FBG_CL_D6_0b": -126500000,
            "FR_FBG_CL_D6_1a": -126500000,
            "FR_FBG_CL_D6_1b": -126500000,
            "FR_FBG_CL_D6_2a": -126500000,
            "FR_FBG_CL_D6_2b": -126500000,
        }
    ]


def test_get_steel_frame_temperature_data(client):
    response = client.get(
        "/fbg/steel-frame/tmp/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2020-02-01T12:00:00",
            "L1": 126.5,
            "L4": 126.5,
            "L7": 126.5,
            "L10": 126.5,
            "L12": 126.5,
            "L14": 126.5,
            "M1": 126.5,
            "M4": 126.5,
            "M7": 126.5,
            "M10": 126.5,
            "M12": 126.5,
            "M14": 126.5,
            "N1": 126.5,
            "N4": 126.5,
            "N7": 126.5,
            "O1": 126.5,
            "O4": 126.5,
            "O6": 126.5,
            "P1": 126.5,
            "P3": 126.5,
            "P5": 126.5,
            "P7": 126.5,
            "P9": 126.5,
            "P11": 126.5,
        }
    ]


def test_get_basement_tmp_data_in_csv_format(client):
    response = client.get(
        "/fbg/basement/tmp/?start-time=2020-02-01T11%3A00%3A00.000000&end-time=2020-02-02T11%3A00%3A00.000000",
        headers={"media-type": "text/csv"},
    )
    assert response.status_code == 200
    assert (
        response.content
        == b"timestamp,BA_FBG_NN01_Tmp_wal05,BA_FBG_NN01_Tmp_wal06,BA_FBG_SS01_Tmp_wal06,BA_FBG_SS01_Tmp_wal05,BA_FBG_SS01_Tmp_wal03,BA_FBG_SS01_Tmp_wal04,BA_FBG_SS01_Tmp_wal02,BA_FBG_SS01_Tmp_wal01,BA_FBG_WW01_Tmp_wal05,BA_FBG_WW01_Tmp_wal06,BA_FBG_EE01_Tmp_wal05,BA_FBG_EE01_Tmp_wal06,BA_FBG_WW01_Tmp_thk05,BA_FBG_WW01_Tmp_thk06,BA_FBG_EE01_Tmp_thk05,BA_FBG_EE01_Tmp_thk06,BA_FBG_SS01_Tmp_thk05,BA_FBG_SS01_Tmp_thk06,BA_FBG_EW01_Tmp_bot03,BA_FBG_EW01_Tmp_top01,BA_FBG_EW01_Tmp_top02,BA_FBG_EW01_Tmp_top03\r\n2020-02-01 12:00:00,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5,126.5\r\n"
    )

