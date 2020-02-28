from fastapi import HTTPException

from .. import Packages
from ..schemas.fbg import DataType


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            raise HTTPException(
                status_code=500, detail=f"Calculation error occured, missing {e}",
            )
        except TypeError as e:
            return None

    return wrapper


@error_handler
def BA_Strain(uid, row, metadata):
    Str_W = getattr(row, uid)
    Str_W0 = metadata[uid].initial_wavelength
    Fg = metadata[uid].coeffs["Fg"]
    try:
        eta = metadata[uid].coeffs["eta"]
    except KeyError:
        eta = 6.3 * 10 ** -6

    tmp_uid = metadata[uid].corresponding_sensor
    delta_T = BA_Temperature(tmp_uid, row, metadata)

    Str_WN = (Str_W - Str_W0) / Str_W0
    return 1e6 * (Str_WN - (eta * delta_T)) / Fg


@error_handler
def BA_Temperature(uid, row, metadata):
    Tmp_W = getattr(row, uid)
    Tmp_W0 = metadata[uid].initial_wavelength
    TS1 = metadata[uid].coeffs["TS1"]
    TS2 = metadata[uid].coeffs["TS2"]

    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return (TS1 * (Tmp_WN ** 2)) + (TS2 * Tmp_WN)


@error_handler
def SF_Strain(uid, row, metadata):
    Str_W = getattr(row, uid)
    Str_W0 = metadata[uid].initial_wavelength
    Fg = metadata[uid].coeffs["Fg"]
    try:
        eta = metadata[uid].coeffs["eta"]
    except KeyError:
        eta = 6.3 * 10 ** -6

    tmp_uid = metadata[uid].corresponding_sensor
    Tmp_W = getattr(row, tmp_uid)
    Tmp_W0 = metadata[tmp_uid].initial_wavelength
    beta = metadata[tmp_uid].coeffs["beta"]

    Str_WN = (Str_W - Str_W0) / Str_W0
    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return 1e6 * (Str_WN - (eta * Tmp_WN / beta)) / Fg


@error_handler
def SF_Temperature(uid, row, metadata):
    Tmp_W = getattr(row, uid)
    Tmp_W0 = metadata[uid].initial_wavelength
    beta = metadata[uid].coeffs["beta"]

    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return Tmp_WN / beta


@error_handler
def FR_Strain(uid, row, metadata):
    Str_W = getattr(row, uid)
    Str_W0 = metadata[uid].initial_wavelength
    Fg = metadata[uid].coeffs["Fg"]
    CTEt = metadata[uid].coeffs["CTEt"]

    tmp_uid = metadata[uid].corresponding_sensor
    Tmp_W = getattr(row, tmp_uid)
    Tmp_W0 = metadata[tmp_uid].initial_wavelength
    St = metadata[tmp_uid].coeffs["St"]

    Str_WN = (Str_W - Str_W0) / Str_W0
    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return 1e6 * ((Str_WN - Tmp_WN) / Fg + Tmp_WN * CTEt / St)


@error_handler
def FR_Temperature(uid, row, metadata):
    Tmp_W = getattr(row, uid)
    Tmp_W0 = metadata[uid].initial_wavelength
    St = metadata[uid].coeffs["St"]

    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return Tmp_WN / St


Calculations = {
    Packages.basement: {
        DataType.strain: BA_Strain,
        DataType.temperature: BA_Temperature,
    },
    Packages.strong_floor: {
        DataType.strain: SF_Strain,
        DataType.temperature: SF_Temperature,
    },
    Packages.steel_frame: {
        DataType.strain: FR_Strain,
        DataType.temperature: FR_Temperature,
    },
}
