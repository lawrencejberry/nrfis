import socket

HOST = "10.0.0.126"
PORT = 1852


class AnalyserClient:
    """
    Client to interact with an sm130 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 1.139 section 4.4.4.5 for details.
    """

    ACKNOWLEDGEMENT_LENGTH = 10  # bytes
    STATUS_HEADER_LENGTH = 88  # bytes

    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.connect((self.host, self.port))

    def end(self):
        self.socket.close()

    def execute(self, command: bytes, override_length: int = None):
        self.socket.sendall(command + b"\n")
        length = int(self.socket.recv(self.ACKNOWLEDGEMENT_LENGTH))
        if length is not None:  # Override message length if provided
            length = override_length
        message = self.socket.recv(length)

        return message

    def get_data(self):
        return self.execute(b"#GET_DATA")

    def get_unbuffered_data(self):
        return self.execute(b"#GET_UNBUFFERED_DATA")

    def get_data_and_levels(self):
        return self.execute(b"#GET_DATA_AND_LEVELS")

    def get_unbuffered_data_and_levels(self):
        return self.execute(b"#GET_UNBUFFERED_DATA_AND_LEVELS")

    def get_spectrum(self):
        return self.execute(b"#GET_SPECTRUM", override_length=65536)

    def get_high_speed_fs(self):
        return self.execute(b"#GET_HIGH_SPEED_FS", override_length=1024)

    def help(self):
        return self.execute(b"#HELP")

    def idn(self):
        return self.execute(b"#IDN?")

    def get_capabilities(self):
        return self.execute(b"#GET_CAPABILITIES")

    def get_sn(self):
        return self.execute(b"#GET_SN")

    def save_settings(self):
        return self.execute(b"#SAVE_SETTINGS")

    def reboot(self):
        return self.execute(b"#REBOOT")

    def set_ip_address(self, address):
        return self.execute(b"#SET_IP_ADDRESS %b" % address)

    def get_ip_address(self):
        return self.execute(b"#GET_IP_ADDRESS")

    def set_ip_netmask(self, mask):
        return self.execute(b"#SET_IP_NETMASK %b" % mask)

    def get_ip_netmask(self):
        return self.execute(b"#GET_IP_NETMASK")

    def set_default_gateway(self, gateway):
        return self.execute(b"#SET_DEFAULT_GATEWAY %b" % gateway)

    def get_default_gateway(self):
        return self.execute(b"#GET_DEFAULT_GATEWAY")

    def set_dhcp(self, val):
        return self.execute(b"#SET_DHCP %b" % val)

    def get_dhcp(self):
        return self.execute(b"#GET_DHCP")

    def restart_network(self):
        return self.execute(b"#RESTART_NETWORK")

    def set_dns_server(self, server):
        return self.execute(b"#SET_DNS_SERVER %b" % server)

    def get_dns_server(self, server):
        return self.execute(b"#GET_DNS_SERVER %b" % server)

    def who(self):
        return self.execute(b"#WHO?")

    def whoami(self):
        return self.execute(b"#WHOAMI?")

    def set_date(self, date):
        return self.execute(b"#SET_DATE %b" % date)

    def set_enable_ntp(self, val):
        return self.execute(b"#SET_ENABLE_NTP %b" % val)

    def get_enable_ntp(self):
        return self.execute(b"#GET_ENABLE_NTP")

    def set_ntp_serverx(self, x, server):
        return self.execute(b"#SET_NTP_SERVER%b %b" % (x, server))

    def get_ntp_serverx(self, x):
        return self.execute(b"#GET_NTP_SERVER%b" % x)

    def get_ch_gain_db(self, ch):
        return self.execute(b"#GET_CH_GAIN_DB %b" % ch)

    def set_ch_gain_db(self, ch, gain):
        return self.execute(b"#SET_CH_GAIN_DB %b %b" % (ch, gain))

    def get_num_dut_channels(self):
        return self.execute(b"#GET_NUM_DUT_CHANNELS")

    def set_ch_noise_thresh(self, ch, val):
        return self.execute(b"#SET_CH_NOISE_THRESH %b %b" % (ch, val))

    def get_ch_noise_thresh(self, ch):
        return self.execute(b"#GET_CH_NOISE_THRESH %b" % ch)

    def set_amp_ch(self, ch):
        return self.execute(b"#SET_AMP_CH %b" % ch)

    def get_amp_ch(self):
        return self.execute(b"#GET_AMP_CH")

    def set_mux_level(self, val):
        return self.execute(b"#SET_MUX_LEVEL %b" % val)

    def get_mux_level(self):
        return self.execute(b"#GET_MUX_LEVEL")

    def set_index_of_refraction(self, ch, val):
        return self.execute(b"#SET_INDEX_OF_REFRACTION %b %b" % (ch, val))

    def get_index_of_refraction(self, ch):
        return self.execute(b"#GET_INDEX_OF_REFRACTION %b" % ch)

    def set_use_references(self, val):
        return self.execute(b"#SET_USE_REFERENCES %b" % val)

    def get_use_references(self):
        return self.execute(b"#GET_USE_REFERENCES")

    def set_reference(self, ch, sensor, refwvl):
        return self.execute(b"#SET_REFERENCE %b %b %b" % (ch, sensor, refwvl))

    def get_reference(self, ch, sensor):
        return self.execute(b"#GET_REFERENCE %b %b" % (ch, sensor))

    def clear_reference(self, ch, sensor):
        return self.execute(b"#CLEAR_REFERENCE %b %b" % (ch, sensor))

    def set_data_rate_divider(self, div):
        return self.execute(b"#SET_DATA_RATE_DIVIDER %b" % div)

    def get_data_rate_divider(self):
        return self.execute(b"#GET_DATA_RATE_DIVIDER")

    def set_data_interleave(self, interleave):
        return self.execute(b"#SET_DATA_INTERLEAVE %b" % interleave)

    def get_data_interleave(self):
        return self.execute(b"#GET_DATA_INTERLEAVE")

    def set_num_averages(self, ch, sensor, avgs):
        return self.execute(b"#SET_NUM_AVERAGES %b %b %b" % (ch, sensor, avgs))

    def get_num_averages(self, ch, sensor):
        return self.execute(b"#GET_NUM_AVERAGES %b %b" % (ch, sensor))

    def set_streaming_data(self, val):
        return self.execute(b"#SET_STREAMING_DATA %b" % val)

    def get_streaming_data(self):
        return self.execute(b"#GET_STREAMING_DATA")

    def set_buffer_enable(self, val):
        return self.execute(b"#SET_BUFFER_ENABLE %b" % val)

    def get_buffer_enable(self):
        return self.execute(b"#GET_BUFFER_ENABLE")

    def get_buffer_count(self):
        return self.execute(b"#GET_BUFFER_COUNT")

    def flush_buffer(self):
        return self.execute(b"#FLUSH_BUFFER")

    def set_operating_mode(self, mode):
        return self.execute(b"#SET_OPERATING_MODE %b" % mode)

    def get_operating_mode(self):
        return self.execute(b"#GET_OPERATING_MODE")

    def set_trig_mode(self, mode):
        return self.execute(b"#SET_TRIG_MODE %b" % mode)

    def get_trig_mode(self):
        return self.execute(b"#GET_TRIG_MODE")

    def set_trig_start_edge(self, val):
        return self.execute(b"#SET_TRIG_START_EDGE %b" % val)

    def get_trig_start_edge(self):
        return self.execute(b"#GET_TRIG_START_EDGE")

    def set_trig_stop_type(self, val):
        return self.execute(b"#SET_TRIG_STOP_TYPE %b" % val)

    def get_trig_stop_type(self):
        return self.execute(b"#GET_TRIG_STOP_TYPE")

    def set_trig_stop_edge(self, val):
        return self.execute(b"#SET_TRIG_STOP_EDGE %b" % val)

    def get_trig_stop_edge(self):
        return self.execute(b"#GET_TRIG_STOP_EDGE")

    def set_trig_num_acq(self, val):
        return self.execute(b"#SET_TRIG_NUM_ACQ %b" % val)

    def get_trig_num_acq(self):
        return self.execute(b"#GET_TRIG_NUM_ACQ")

    def set_auto_retrig(self, val):
        return self.execute(b"#SET_AUTO_RETRIG %b" % val)

    def get_auto_retrig(self):
        return self.execute(b"#GET_AUTO_RETRIG")

    def sw_trig_start(self):
        return self.execute(b"#SW_TRIG_START")

    def sw_trig_stop(self):
        return self.execute(b"#SW_TRIG_STOP")

    def measure_locations(self):
        return self.execute(b"#MEASURE_LOCATIONS")

    def apply_measured_locations(self, ch, sensor):
        return self.execute(b"#APPLY_MEASURED_LOCATIONS %b %b" % (ch, sensor))

    def get_measured_location(self, ch, sensor):
        return self.execute(b"#GET_MEASURED_LOCATION %b %b" % (ch, sensor))

    def set_loc_meas_ch_offset_meters(self, ch, val):
        return self.execute(b"#SET_LOC_MEAS_CH_OFFSET_METERS %b %b" % (ch, val))

    def set_sensor_location(self, ch, sensor, val):
        return self.execute(b"#SET_SENSOR_LOCATION %b %b %b" % (ch, sensor, val))

    def get_sensor_location(self, ch, sensor):
        return self.execute(b"#GET_SENSOR_LOCATION %b %b" % (ch, sensor))
