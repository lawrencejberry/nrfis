import sys
import os
import logging
import logging.handlers

from wx import ListItem, ColourDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_models import (
    Base,
    basement_package,
    strong_floor_package,
    steel_frame_package,
)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class CustomConsoleHandler(logging.StreamHandler):
    def __init__(self, listctrl):
        logging.StreamHandler.__init__(self)
        self.listctrl = listctrl

        colours = ColourDatabase()
        self.colours = {
            "CRITICAL": colours.Find("RED"),
            "ERROR": colours.Find("MEDIUM VIOLET RED"),
            "WARNING": colours.Find("YELLOW"),
            "INFO": colours.Find("YELLOW GREEN"),
            "DEBUG": colours.Find("MEDIUM GOLDENROD"),
        }

    def emit(self, record):
        item = ListItem()
        item.SetText(self.format(record))
        item.SetBackgroundColour(
            self.colours.get(record.levelname, self.colours["CRITICAL"])
        )
        item.SetId(self.listctrl.GetItemCount())
        if self.listctrl.ItemCount > 200:
            self.listctrl.DeleteItem(0)
        self.listctrl.InsertItem(item)
        self.flush()


# Create logger
os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fileHandler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(ROOT_DIR, "logs/data_collection_system.log"), when="midnight", utc=True
)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


# Create database engine
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./backend/data_collection_system/tests/.test.db"
)
db = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(db)
