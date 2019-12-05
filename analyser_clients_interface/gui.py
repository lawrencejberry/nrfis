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
        self.title = wx.StaticText(self, wx.ID_ANY, "Analyser 1 ")
        self.host_label = wx.StaticText(self, wx.ID_ANY, "Host: ")
        self.host = wx.TextCtrl(self, wx.ID_ANY, self.client.host)
        self.port_label = wx.StaticText(self, wx.ID_ANY, "Port: ")
        self.port = wx.TextCtrl(self, wx.ID_ANY, str(self.client.port))
        self.connect = wx.Button(self, wx.ID_ANY, "Connect")
        self.stream = wx.Button(self, wx.ID_ANY, "Start streaming")
        self.stream.Disable()  # Streaming button disabled until client has connected

        # Status information
        self.status_labels = {
            "fs_radix": "FS Radix ",
            "fw_version": "FW Version ",
            "primary_fan": "Primary Fan ",
            "secondary_fan": "Secondary Fan ",
            "calibration_fault": "Calibration Fault ",
            "switch_position": "Switch Position ",
            "mux_level": "MUX Level",
            "triggering_mode": "Triggering Mode ",
            "operating_mode": "Operating Mode ",
            "num_peaks_detected": "Number of Peaks Detected ",
            "error": "Error ",
            "buffer": "Buffer ",
            "header_version": "Header Version ",
            "granularity": "Granularity ",
            "full_spectrum_start_wvl": "Full Spectrum Start Wavelength ",
            "full_spectrum_end_wvl": "Full Spectrum End Wavelength ",
        }
        self.fs_radix = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.fw_version = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.primary_fan = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.secondary_fan = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.calibration_fault = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.switch_position = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.mux_level = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.triggering_mode = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.operating_mode = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.num_peaks_detected = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.error = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.buffer = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.header_version = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.granularity = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.full_spectrum_start_wvl = wx.StaticText(self, wx.ID_ANY, "Not acquired ")
        self.full_spectrum_end_wvl = wx.StaticText(self, wx.ID_ANY, "Not acquired ")

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        AsyncBind(wx.EVT_BUTTON, self.on_connect, self.connect)
        AsyncBind(wx.EVT_BUTTON, self.on_stream, self.stream)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        client_sizer = wx.BoxSizer(wx.VERTICAL)
        status_sizer = wx.GridSizer(16, 2, 0, 10)

        main_sizer.Add(client_sizer)

        client_sizer.Add(self.title, 0, wx.ALL, 5)
        client_sizer.Add(self.host_label, 0, wx.ALL, 5)
        client_sizer.Add(self.host, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(self.port_label, 0, wx.ALL, 5)
        client_sizer.Add(self.port, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(self.connect, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(self.stream, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(status_sizer, 0, wx.ALL | wx.EXPAND, 5)

        for status in self.status_labels:
            status_sizer.Add(
                wx.StaticText(self, wx.ID_ANY, self.status_labels[status]), 0, wx.ALL, 5
            )
            status_sizer.Add(getattr(self, status), 0, wx.ALL, 5)

        self.SetSizeHints(600, 600)  # Sets the minimum window size
        self.SetSizer(main_sizer)

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
            await self.update_status()
            self.stream.Enable()

    async def on_stream(self, event):
        """Handle the event when the user clicks the start/stop streaming button."""
        if self.client.streaming:
            self.stream.SetLabel("Start streaming")
            self.client.streaming = False
        else:
            self.stream.SetLabel("Stop streaming")
            await self.client.record()

    async def update_status(self):
        await self.client.update_status()
        for status in self.status_labels:
            getattr(self, status).SetLabel(f"{str(getattr(self.client, status))} ")
