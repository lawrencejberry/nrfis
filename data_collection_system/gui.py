from asyncio import sleep

import wx
from wxasync import AsyncBind

from .x55.x55_client import x55Client

SAMPLING_RATE_CHOICES = ["1", "10", "100", "1000"]
CONFIGURATION_CHOICES = ["Basement and Frame", "Strong Floor"]


class Gui(wx.Frame):
    """
    Configure the main window and all the widgets.
    This class provides a graphical user interface for the data collection system and
    enables the user to start and stop data streaming from an x55 client.
    """

    def __init__(self):
        """Initialise widgets and layout."""
        super().__init__(
            parent=None, title="IRIS Data Collection System", size=(1000, 800)
        )

        # Initialise client
        self.client = x55Client()

        # Configure the file menu
        file_menu = wx.Menu()
        menu_bar = wx.MenuBar()
        file_menu.Append(wx.ID_ABOUT, "About")
        file_menu.Append(wx.ID_EXIT, "Quit")
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

        # Configure the widgets
        self.title = wx.StaticText(self, wx.ID_ANY, self.client.name)
        self.connect = wx.Button(self, wx.ID_ANY, "Connect")
        self.stream = wx.Button(self, wx.ID_ANY, "Start streaming")
        self.stream.Disable()  # Streaming button disabled until client has connected
        self.host = wx.TextCtrl(self, wx.ID_ANY, self.client.host)
        self.configuration = wx.Choice(self, wx.ID_ANY, choices=CONFIGURATION_CHOICES)
        self.configuration.SetSelection(self.client.configuration)
        self.sampling_rate = wx.Choice(self, wx.ID_ANY, choices=SAMPLING_RATE_CHOICES)
        self.sampling_rate.SetSelection(
            self.sampling_rate.FindString(str(self.client.sampling_rate))
        )
        self.sampling_rate.Disable()

        # Status information
        self.statuses = {
            "instrument_name": "Instrument name",
            "firmware_version": "Firmware version",
            "is_ready": "Ready",
            "dut_channel_count": "DUT channel count",
            "peak_data_streaming_status": "Streaming status",
            "peak_data_streaming_divider": "Streaming divider",
            "peak_data_streaming_available_buffer": "Available streaming buffer",
            "laser_scan_speed": "Laser scan speed",
            "instrument_time": "Instrument time",
            "ntp_enabled": "NTP server enabled",
        }
        for status in self.statuses:
            setattr(self, status, wx.StaticText(self, wx.ID_ANY, "None"))

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        AsyncBind(wx.EVT_BUTTON, self.on_connect, self.connect)
        AsyncBind(wx.EVT_BUTTON, self.on_stream, self.stream)
        AsyncBind(wx.EVT_CHOICE, self.on_change_sampling_rate, self.sampling_rate)
        AsyncBind(wx.EVT_CHOICE, self.on_change_configuration, self.configuration)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        client_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.GridSizer(3, 2, 0, 10)
        status_sizer = wx.GridSizer(len(self.statuses), 2, 0, 10)

        main_sizer.Add(client_sizer)

        client_sizer.Add(self.title, 0, wx.ALL, 5)
        client_sizer.Add(self.connect, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(self.stream, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(control_sizer, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(status_sizer, 0, wx.ALL | wx.EXPAND, 5)

        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Host:"), 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            self.host, 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Configuration:"), 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            self.configuration, 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Sampling rate:"), 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            self.sampling_rate, 0, wx.ALL | wx.EXPAND, 5,
        )

        for status in self.statuses:
            status_sizer.Add(
                wx.StaticText(self, wx.ID_ANY, self.statuses[status]),
                0,
                wx.ALL | wx.EXPAND,
                5,
            )
            status_sizer.Add(getattr(self, status), 0, wx.ALL | wx.EXPAND, 5)

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
        if self.client.conn.command.active:
            await self.client.conn.command.disconnect()
            self.connect.SetLabel("Connect")
            self.stream.Disable()
            self.sampling_rate.Disable()
        else:
            await self.client.conn.command.connect()
            self.connect.SetLabel("Disconnect")
            self.stream.Enable()
            self.sampling_rate.Enable()
            await self.update_status()

    async def on_stream(self, event):
        """Handle the event when the user clicks the start/stop streaming button."""
        if self.client.streaming:
            self.stream.SetLabel("Start streaming")
            self.client.streaming = False
        else:
            self.stream.SetLabel("Stop streaming")
            await self.client.record()

    async def on_change_sampling_rate(self, event):
        """Handle the event when the user changes the sampling rate control
        value. """
        sampling_rate = int(
            self.sampling_rate.GetString(self.sampling_rate.GetSelection())
        )
        status = await self.client.update_sampling_rate(sampling_rate)
        if not status:  # If unsuccessful, revert to original selection
            self.sampling_rate.SetSelection(
                self.sampling_rate.FindString(str(self.client.sampling_rate))
            )

    async def on_change_configuration(self, event):
        """Handle the event when the user changes the configuration control
        value. """
        status = await self.client.update_configuration(
            self.configuration.GetSelection()
        )
        if not status:  # If unsuccessful, revert to original selection
            self.configuration.SetSelection(
                self.sampling_rate.FindString(str(self.client.sampling_rate))
            )

    async def update_status(self):
        while self.client.conn.command.active:
            await self.client.update_status()
            for status in self.statuses:
                getattr(self, status).SetLabel(f"{str(getattr(self.client, status))} ")
            await sleep(1)
