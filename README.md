# National Research Facility for Infrastructure Sensing - Information System
![](https://github.com/lawrence-b/nrfis/workflows/Data%20Collection%20System/badge.svg)
![](https://github.com/lawrence-b/nrfis/workflows/Web%20Server/badge.svg)
[![codecov](https://codecov.io/gh/lawrence-b/nrfis/branch/master/graph/badge.svg?token=yzF2kxTgQs)](https://codecov.io/gh/lawrence-b/nrfis)

## Data Collection System

The _Data Collection System_ is a Python package which connects to and records sensor data from a variety of optical instruments. At the moment only a single si255 optical instrument is enabled. It features a graphical user interface from which the user can connect to this optical instrument, see various status information, upload a particular configuration and start/stop recording.

### To install:
```
source venv/bin/activate  # Activate virtual environment
pip install -r backend/requirements.txt -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04
```

### To run:
```
export DATABASE_URL=postgresql+psycopg2://postgres:fourth-year@localhost/nrfisdb
source venv/bin/activate  # Activate virtual environment
python -m backend.data_collection_system
```

The export command is unnecessary if the `DATABASE_URL` environment variable is also specified in `~.profile`.

### To run tests locally:
```
source venv/bin/activate  # Activate virtual environment
export DATABASE_URL="sqlite:///./backend/data_collection_system/tests/.test.db"
pytest backend/data_collection_system
```

## Web Server

The _Web Server_ is a Python [FastAPI](https://fastapi.tiangolo.com) application which allows users to access past sensor data via a REST API.

### To install:
```
sudo docker build -t web_server_image -f backend/web_server/Dockerfile ./backend
```

### To run:
```
sudo docker run -d --name web_server_container -p 80:80 --restart always --network="host" --env DATABASE_URL=postgresql+psycopg2://postgres:fourth-year@127.0.0.1/nrfisdb web_server_image
```
To run against a local test database substitute in your own `DATABASE_URL`.

### To run tests locally:
```
source venv/bin/activate  # Activate virtual environment
pytest backend/web_server
```