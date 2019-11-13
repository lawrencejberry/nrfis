import asyncio
from asyncio.events import get_event_loop

import wx
from wxasync import WxAsyncApp

from gui import Gui


def main():
    app = WxAsyncApp()
    gui: Gui = Gui()
    gui.Show()
    gui.Maximize()
    loop = get_event_loop()
    loop.run_until_complete(app.MainLoop())


if __name__ == "__main__":
    main()
