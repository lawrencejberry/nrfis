import logging
from asyncio import sleep

import wx
from wx.lib.mixins import listctrl
from wxasync import AsyncBind

from . import logger, logFormatter
from .x55.x55_client import (
    x55Client,
    SetupOptions,
)


class CustomConsoleHandler(logging.StreamHandler):
    def __init__(self, ctrl):
        logging.StreamHandler.__init__(self)
        self.listctrl = ctrl

        colours = wx.ColourDatabase()
        self.colours = {
            "CRITICAL": colours.Find("RED"),
            "ERROR": colours.Find("MEDIUM VIOLET RED"),
            "WARNING": colours.Find("YELLOW"),
            "INFO": colours.Find("YELLOW GREEN"),
            "DEBUG": colours.Find("MEDIUM GOLDENROD"),
        }

    def emit(self, record):
        item = wx.ListItem()
        item.SetText(self.format(record))
        item.SetBackgroundColour(
            self.colours.get(record.levelname, self.colours["CRITICAL"])
        )
        item.SetId(self.listctrl.GetItemCount())
        if self.listctrl.ItemCount > 200:
            self.listctrl.DeleteItem(0)
        self.listctrl.InsertItem(item)
        self.flush()


class LogList(wx.ListCtrl, listctrl.ListCtrlAutoWidthMixin):
    def __init__(
        self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0
    ):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listctrl.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)
        self.InsertColumn(0, heading="Log")
        self.SetFont(wx.Font(13, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
        txtHandler = CustomConsoleHandler(self)
        txtHandler.setFormatter(logFormatter)
        logger.addHandler(txtHandler)


class Gui(wx.Frame):
    """
    Configure the main window and all the widgets.
    This class provides a graphical user interface for the data collection system and
    enables the user to start and stop data streaming from an x55 client.
    """

    def __init__(self):
        """Initialise widgets and layout."""
        super().__init__(
            parent=None, title="NRFIS Data Collection System", size=(1000, 800)
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
        self.configuration = wx.Button(self, wx.ID_ANY, "Upload config file")
        self.host = wx.TextCtrl(self, wx.ID_ANY, self.client.host)
        self.setup = wx.Choice(
            self, wx.ID_ANY, choices=[str(option) for option in SetupOptions]
        )
        self.setup.SetSelection(self.client.configuration.setup)
        self.laser_scan_speed_choice = wx.Choice(
            self,
            wx.ID_ANY,
            choices=[str(x) for x in self.client.available_laser_scan_speeds],
        )
        self.laser_scan_speed_choice.Disable()
        self.divider = wx.Choice(
            self, wx.ID_ANY, choices=[str(x) for x in self.client.divider_options]
        )
        self.divider.Disable()

        # Status information
        self.statuses = {
            "instrument_name": "Instrument name",
            "firmware_version": "Firmware version",
            "is_ready": "Ready",
            "dut_channel_count": "DUT channel count",
            "peak_data_streaming_status": "Streaming status",
            "laser_scan_speed": "Laser scan speed",
            "peak_data_streaming_divider": "Streaming divider",
            "effective_sampling_rate": "Effective sampling rate",
            "peak_data_streaming_available_buffer": "Available streaming buffer",
            "instrument_time": "Instrument time",
            "ntp_enabled": "NTP server enabled",
        }
        for status in self.statuses:
            setattr(self, status, wx.StaticText(self, wx.ID_ANY, "None"))

        # Log widget
        self.log = LogList(self, wx.ID_ANY, size=(300, 100), style=wx.LC_REPORT)

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        AsyncBind(wx.EVT_BUTTON, self.on_connect, self.connect)
        AsyncBind(wx.EVT_BUTTON, self.on_stream, self.stream)
        AsyncBind(wx.EVT_BUTTON, self.on_configuration, self.configuration)
        AsyncBind(wx.EVT_TEXT, self.on_change_host, self.host)
        AsyncBind(
            wx.EVT_CHOICE, self.on_change_laser_scan_speed, self.laser_scan_speed_choice
        )
        AsyncBind(wx.EVT_CHOICE, self.on_change_divider, self.divider)
        AsyncBind(wx.EVT_CHOICE, self.on_change_setup, self.setup)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        client_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.GridSizer(4, 2, 0, 10)
        status_sizer = wx.GridSizer(len(self.statuses), 2, 0, 10)
        log_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self)

        main_sizer.Add(client_sizer, 0.5, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(log_sizer, 1, wx.ALL | wx.EXPAND, 5)

        client_sizer.Add(self.title, 0, wx.ALL, 5)
        client_sizer.Add(self.connect, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(self.stream, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(self.configuration, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(control_sizer, 0, wx.ALL | wx.EXPAND, 5)
        client_sizer.Add(status_sizer, 0, wx.ALL | wx.EXPAND, 5)

        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Host:"), 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            self.host, 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Laser scan speed (Hz):"),
            0,
            wx.ALL | wx.EXPAND,
            5,
        )
        control_sizer.Add(
            self.laser_scan_speed_choice, 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Peak data streaming divider:"),
            0,
            wx.ALL | wx.EXPAND,
            5,
        )
        control_sizer.Add(
            self.divider, 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            wx.StaticText(self, wx.ID_ANY, "Setup:"), 0, wx.ALL | wx.EXPAND, 5,
        )
        control_sizer.Add(
            self.setup, 0, wx.ALL | wx.EXPAND, 5,
        )

        for status in self.statuses:
            status_sizer.Add(
                wx.StaticText(self, wx.ID_ANY, self.statuses[status]),
                0,
                wx.ALL | wx.EXPAND,
                5,
            )
            status_sizer.Add(getattr(self, status), 0, wx.ALL | wx.EXPAND, 5)

        log_sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)

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
                "A program that records sensor data from an si255 optical instrument and stores it in a permanent database. The user can see live status information, upload a particular Enlight configuration file and start/stop recording the received data.\n\nDeveloped by Lawrence Berry for a IIB Master's Project, 2019-2020",
                "About",
                wx.ICON_INFORMATION | wx.OK,
            )

    async def on_connect(self, event):
        """Handle the event when the user clicks the connect/disconnect button."""
        if self.client.connected:
            await self.client.disconnect()
            self.connect.SetLabel("Connect")
            self.stream.Disable()
            self.host.Disable()
            self.laser_scan_speed_choice.Disable()
            self.divider.Disable()
        else:
            await self.client.connect()
            self.connect.SetLabel("Disconnect")
            self.stream.Enable()
            self.host.Enable()
            self.laser_scan_speed_choice.Enable()
            self.divider.Enable()
            await self.update_status()

    async def on_stream(self, event):
        """Handle the event when the user clicks the start/stop streaming button."""
        if self.client.streaming:
            self.stream.SetLabel("Start streaming")
            self.client.streaming = False
        else:
            self.stream.SetLabel("Stop streaming")
            await self.client.record()

    async def on_configuration(self, event):
        if (
            wx.MessageBox(
                f"This will overwrite the configuration for {str(self.client.configuration.setup)}.",
                "Warning",
                wx.ICON_QUESTION | wx.YES_NO,
                self,
            )
            == wx.NO
        ):
            return

        # otherwise ask the user what new file to open
        with wx.FileDialog(
            self,
            "Upload Enlight config file",
            wildcard="MOI files (*.moi)|*.moi",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, "r") as file:
                    self.client.configuration.parse(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % file)

    async def on_change_host(self, event):
        self.client.host = self.host.GetValue()

    async def on_change_laser_scan_speed(self, event):
        """Handle the event when the user changes the laser scan speed control
        value. """
        try:
            laser_scan_speed = int(event.GetString())
        except ValueError:
            logger.warning("Invalid laser scan speed: %s", event.GetString())
            return

        self.laser_scan_speed_choice.SetSelection(
            self.laser_scan_speed_choice.FindString(
                str(await self.client.update_laser_scan_speed(laser_scan_speed))
            )
        )

    async def on_change_divider(self, event):
        """Handle the event when the user changes the peak data streaming divider control
        value. """
        try:
            divider = int(event.GetString())
        except ValueError:
            logger.warning("Invalid peak data streaming divider: %s", event.GetString())
            return

        self.divider.SetSelection(
            self.divider.FindString(
                str(await self.client.update_peak_data_streaming_divider(divider))
            )
        )

    async def on_change_setup(self, event):
        """Handle the event when the user changes the setup control
        value. """
        status = await self.client.update_setup(SetupOptions(event.GetInt()))
        if not status:  # If unsuccessful, revert to original selection
            self.setup.SetSelection(
                self.setup.FindString(str(self.client.configuration.setup))
            )

    async def update_status(self):
        while self.client.connected:
            if self.client.command.reading.locked():
                await sleep(0.1)
                continue

            await self.client.update_status()
            for status in self.statuses:
                getattr(self, status).SetLabel(f"{str(getattr(self.client, status))} ")
            self.laser_scan_speed_choice.Set(
                [str(x) for x in self.client.available_laser_scan_speeds]
            )
            self.laser_scan_speed_choice.SetSelection(
                self.laser_scan_speed_choice.FindString(
                    str(self.client.laser_scan_speed)
                )
            )
            self.divider.SetSelection(
                self.divider.FindString(str(self.client.peak_data_streaming_divider))
            )
            await sleep(1)
