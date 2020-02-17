from . import Packages
from .schemas.fbg import DataType


def BA_SF_Strain(uid, row, metadata):
    Str_W = getattr(row, uid)
    Str_W0 = metadata[uid].initial_wavelength
    Fg = metadata[uid].Fg
    eta = metadata[uid].eta

    tmp_uid = metadata[uid].corresponding_sensor
    Tmp_W = getattr(row, tmp_uid)
    Tmp_W0 = metadata[tmp_uid].initial_wavelength
    beta = metadata[tmp_uid].beta

    Str_WN = (Str_W - Str_W0) / Str_W0
    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return 1e6 * (Str_WN - (eta * Tmp_WN / beta)) / Fg


def BA_SF_Temperature(uid, row, metadata):
    Tmp_W = getattr(row, uid)
    Tmp_W0 = metadata[uid].initial_wavelength
    beta = metadata[uid].beta

    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return Tmp_WN / beta


def FR_Strain(uid, row, metadata):
    Str_W = getattr(row, uid)
    Str_W0 = metadata[uid].initial_wavelength
    Fg = metadata[uid].Fg
    CTEt = metadata[uid].CTEt

    tmp_uid = metadata[uid].corresponding_sensor
    Tmp_W = getattr(row, tmp_uid)
    Tmp_W0 = metadata[tmp_uid].initial_wavelength
    St = metadata[tmp_uid].St

    Str_WN = (Str_W - Str_W0) / Str_W0
    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return 1e6 * ((Str_WN - Tmp_WN) / Fg + Tmp_WN * CTEt / St)


def FR_Temperature(uid, row, metadata):
    Tmp_W = getattr(row, uid)
    Tmp_W0 = metadata[uid].initial_wavelength
    St = metadata[uid].St

    Tmp_WN = (Tmp_W - Tmp_W0) / Tmp_W0
    return Tmp_WN / St


Calculations = {
    Packages.basement: {
        DataType.strain: BA_SF_Strain,
        DataType.temperature: BA_SF_Temperature,
    },
    Packages.strong_floor: {
        DataType.strain: BA_SF_Strain,
        DataType.temperature: BA_SF_Temperature,
    },
    Packages.steel_frame: {
        DataType.strain: FR_Strain,
        DataType.temperature: FR_Temperature,
    },
}
