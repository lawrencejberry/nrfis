def calculate_uncompensated_strain(str_wvl, initial_str_wvl, Fg):
    normalised_str_wavelength = (str_wvl - initial_str_wvl) / initial_str_wvl
    return (1e6 * normalised_str_wavelength) / Fg


def calculate_temperature_compensated_strain(
    str_wvl, initial_str_wvl, tmp_wvl, initial_tmp_wvl, Fg, St, CTEt, CTEs
):
    normalised_str_wavelength = (str_wvl - initial_str_wvl) / initial_str_wvl
    normalised_tmp_wavelength = (tmp_wvl - initial_tmp_wvl) / initial_tmp_wvl
    delta_T = normalised_tmp_wavelength / St
    EpsT0 = delta_T * (CTEs - CTEt + (1e6 * (St / Fg)))
    return (1e6 * normalised_str_wavelength / Fg) - EpsT0
