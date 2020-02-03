def calculate_uncompensated_strain(str_wvl, initial_str_wvl, gauge_factor):
    normalised_str_wavelength = (str_wvl - initial_str_wvl) / initial_str_wvl
    return (1e6 * normalised_str_wavelength) / gauge_factor


def calculate_temperature_compensated_strain(
    str_wvl, initial_str_wvl, tmp_wvl, initial_tmp_wvl, gauge_factor
):
    normalised_str_wavelength = (str_wvl - initial_str_wvl) / initial_str_wvl
    normalised_tmp_wavelength = (tmp_wvl - initial_tmp_wvl) / initial_tmp_wvl
    return 1e6 * (normalised_str_wavelength - normalised_tmp_wavelength) / gauge_factor
