import wx
from wxasync import AsyncBind

from client import x30Client


class Gui(wx.Frame):
    """
    Configure the main window and all the widgets.
    This class provides a graphical user interface for the analyser client and
    enables the user to start and stop data streaming.
    """

    def __init__(self):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title="IRIS Analyser Client", size=(1000, 800))

        # Initialise client
        self.client = x30Client()

        # Configure the file menu
        file_menu = wx.Menu()
        menu_bar = wx.MenuBar()
        file_menu.Append(wx.ID_ABOUT, "About")
        file_menu.Append(wx.ID_EXIT, "Quit")
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

        # Configure the widgets
        self.label = wx.StaticText(self, wx.ID_ANY, "Analyser 1")
        self.title = wx.StaticText(self, wx.ID_ANY, "")
        self.host = wx.TextCtrl(self, wx.ID_ANY, "")
        self.port = wx.TextCtrl(self, wx.ID_ANY, "")
        self.connect = wx.Button(self, wx.ID_ANY, "Connect")
        self.stream = wx.Button(self, wx.ID_ANY, "Start streaming")
        self.stream.Disable()  # Streaming button disabled until client has connected

        # Status information
        self.fs_radix = wx.StaticText(self, wx.ID_ANY, "FS Radix:")
        self.fw_version = wx.StaticText(self, wx.ID_ANY, "FW version:")
        self.primary_fan = wx.StaticText(self, wx.ID_ANY, "Primary fan:")
        self.secondary_fan = wx.StaticText(self, wx.ID_ANY, "Secondary fan:")
        self.calibration_fault = wx.StaticText(self, wx.ID_ANY, "Calibration fault:")
        self.switch_position = wx.StaticText(self, wx.ID_ANY, "Switch position:")
        self.mux_level = wx.StaticText(self, wx.ID_ANY, "MUX level:")
        self.triggering_mode = wx.StaticText(self, wx.ID_ANY, "Triggering mode:")
        self.operating_mode = wx.StaticText(self, wx.ID_ANY, "Operating mode:")
        self.num_peaks_detected = wx.StaticText(
            self, wx.ID_ANY, "Number of peaks detected:"
        )
        self.error = wx.StaticText(self, wx.ID_ANY, "Error:")
        self.buffer = wx.StaticText(self, wx.ID_ANY, "Buffer:")
        self.header_version = wx.StaticText(self, wx.ID_ANY, "Header version:")
        self.granularity = wx.StaticText(self, wx.ID_ANY, "Granularity:")
        self.full_spectrum_start_wvl = wx.StaticText(
            self, wx.ID_ANY, "Full spectrum start wavelength:"
        )
        self.full_spectrum_end_wvl = wx.StaticText(
            self, wx.ID_ANY, "Full spectrum end wavelength:"
        )

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        AsyncBind(wx.EVT_BUTTON, self.on_connect, self.connect)
        AsyncBind(wx.EVT_BUTTON, self.on_stream, self.stream)

        # Configure sizers for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.ALL, 5)
        sizer.Add(self.title, 0, wx.ALL, 5)
        sizer.Add(self.host, 0, wx.ALL, 5)
        sizer.Add(self.port, 0, wx.ALL, 5)
        sizer.Add(self.connect, 0, wx.ALL, 5)
        sizer.Add(self.stream, 0, wx.ALL, 5)
        sizer.Add(self.fs_radix, 0, wx.ALL, 5)
        sizer.Add(self.fw_version, 0, wx.ALL, 5)
        sizer.Add(self.primary_fan, 0, wx.ALL, 5)
        sizer.Add(self.secondary_fan, 0, wx.ALL, 5)
        sizer.Add(self.calibration_fault, 0, wx.ALL, 5)
        sizer.Add(self.switch_position, 0, wx.ALL, 5)
        sizer.Add(self.mux_level, 0, wx.ALL, 5)
        sizer.Add(self.triggering_mode, 0, wx.ALL, 5)
        sizer.Add(self.operating_mode, 0, wx.ALL, 5)
        sizer.Add(self.num_peaks_detected, 0, wx.ALL, 5)
        sizer.Add(self.error, 0, wx.ALL, 5)
        sizer.Add(self.buffer, 0, wx.ALL, 5)
        sizer.Add(self.header_version, 0, wx.ALL, 5)
        sizer.Add(self.granularity, 0, wx.ALL, 5)
        sizer.Add(self.full_spectrum_start_wvl, 0, wx.ALL, 5)
        sizer.Add(self.full_spectrum_end_wvl, 0, wx.ALL, 5)

        self.SetSizeHints(600, 600)  # Sets the minimum window size
        self.SetSizer(sizer)

        # Add tooltips
        self.connect.SetToolTip("Connect/disconnect to the specified host and port")
        self.stream.SetToolTip("Start/stop streaming data from specified analyser")

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        event_id = event.GetId()
        if event_id == wx.ID_EXIT:
            self.Close(True)
        elif event_id == wx.ID_ABOUT:
            wx.MessageBox(
                "IRIS Analyser Client\nLawrence Berry",
                "About IRIS",
                wx.ICON_INFORMATION | wx.OK,
            )

    async def on_connect(self, event):
        """Handle the event when the user clicks the connect/disconnect button."""
        if self.client.connected:
            await self.client.disconnect()
            self.connect.SetLabel("Connect")
            self.stream.Disable()
        else:
            await self.client.connect()
            self.connect.SetLabel("Disconnect")
            self.update_status_information()
            self.stream.Enable()

    async def on_stream(self, event):
        """Handle the event when the user clicks the start/stop streaming button."""
        if self.client.streaming:
            self.client.streaming = False
            self.stream.SetLabel("Start streaming")
        else:
            await self.client.stream_data()
            self.stream.SetLabel("Stop streaming")

    def update_status_information(self):
        self.fs_radix = wx.StaticText(
            self, wx.ID_ANY, f"FS Radix:{self.client.fs_radix}"
        )
        self.fw_version = wx.StaticText(
            self, wx.ID_ANY, f"FW version: {self.client.fw_version}"
        )
        self.primary_fan = wx.StaticText(
            self, wx.ID_ANY, f"Primary fan: {self.client.primary_fan}"
        )
        self.secondary_fan = wx.StaticText(
            self, wx.ID_ANY, f"Secondary fan: {self.client.secondary_fan}"
        )
        self.calibration_fault = wx.StaticText(
            self, wx.ID_ANY, f"Calibration fault: {self.client.calibration_fault}"
        )
        self.switch_position = wx.StaticText(
            self, wx.ID_ANY, f"Switch position: {self.client.switch_position}"
        )
        self.mux_level = wx.StaticText(
            self, wx.ID_ANY, f"MUX level: {self.client.mux_level}"
        )
        self.triggering_mode = wx.StaticText(
            self, wx.ID_ANY, f"Triggering mode: {self.client.triggering_mode}"
        )
        self.operating_mode = wx.StaticText(
            self, wx.ID_ANY, f"Operating mode: {self.client.operating_mode}"
        )
        self.num_peaks_detected = wx.StaticText(
            self,
            wx.ID_ANY,
            f"Number of peaks detected: {self.client.num_peaks_detected}",
        )
        self.error = wx.StaticText(self, wx.ID_ANY, f"Error: {self.client.error}")
        self.buffer = wx.StaticText(self, wx.ID_ANY, f"Buffer: {self.client.buffer}")
        self.header_version = wx.StaticText(
            self, wx.ID_ANY, f"Header version: {self.client.header_version}"
        )
        self.granularity = wx.StaticText(
            self, wx.ID_ANY, f"Granularity: {self.client.granularity}"
        )
        self.full_spectrum_start_wvl = wx.StaticText(
            self,
            wx.ID_ANY,
            f"Full spectrum start wavelength: {self.client.full_spectrum_start_wvl}",
        )
        self.full_spectrum_end_wvl = wx.StaticText(
            self,
            wx.ID_ANY,
            f"Full spectrum end wavelength: {self.client.full_spectrum_end_wvl}",
        )
