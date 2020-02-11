from asyncio.events import get_event_loop

from wxasync import WxAsyncApp

from .gui import Gui

app = WxAsyncApp()
gui: Gui = Gui()
gui.Show()
gui.Maximize()
loop = get_event_loop()
loop.run_until_complete(app.MainLoop())
