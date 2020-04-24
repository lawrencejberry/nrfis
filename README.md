# National Research Facility for Infrastructure Sensing - Information System

![](https://github.com/lawjb/nrfis/workflows/Data%20Collection%20System%20Tests/badge.svg)
![](https://github.com/lawjb/nrfis/workflows/Web%20Server%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/lawjb/nrfis/branch/master/graph/badge.svg?token=yzF2kxTgQs)](https://codecov.io/gh/lawjb/nrfis)

## Data Collection System

The _Data Collection System_ is a Python package which connects to and records sensor data from a variety of optical instruments. At the moment only a single si255 optical instrument is enabled. It features a graphical user interface from which the user can connect to this optical instrument, see various status information, upload a particular configuration and start/stop recording.

Please note that the si255 instrument obtains the time from NRFIS Ubuntu computer when it connects. The computer must therefore be set to the Etc/UTC timezone to ensure the instrument time is also always UTC.

### To install:

```
source venv/bin/activate  # Activate virtual environment
pip install -r backend/requirements.txt -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04
```

### To run in development and production:

```
export PYTHONPATH=`pwd`/backend
export DATABASE_URL=postgresql+psycopg2://postgres:<password>@localhost/nrfisdb
source venv/bin/activate  # Activate virtual environment
python -m data_collection_system
```

Substitute in the database password, currently known to Lawrence Berry and Paul Fidler.

To run against a local test database substitute in your own `DATABASE_URL`. This environment variable can also be set automatically by placing it in your bash profile e.g. `~.profile`.

### To run tests locally:

```
export PYTHONPATH=`pwd`
export DATABASE_URL="sqlite:///./backend/data_collection_system/tests/.test.db"
source venv/bin/activate  # Activate virtual environment
pytest backend/data_collection_system
```

## Web Server

The _Web Server_ is a Python [FastAPI](https://fastapi.tiangolo.com) application which allows users to access past sensor data via a REST API and accompanying website. The API can be accessed from within the Enginering network at: http://129.169.72.175, and the website at: http://129.169.72.175/docs.

### To install:

```
sudo docker build -t web_server_image -f backend/web_server/Dockerfile ./backend
```

### To run in development:

```
export DATABASE_URL=postgresql+psycopg2://postgres:<password>@127.0.0.1/nrfisdb
cd backend
uvicorn web_server.main:app --reload
```

Substitute in the database password, currently known to Lawrence Berry and Paul Fidler.

To run against a local test database substitute in your own `DATABASE_URL`. This environment variable can also be set automatically by placing it in your bash profile e.g. `~.profile`.

### To run in production:

```
sudo docker run -d --name web_server_container -p 80:80 --restart always --network="host" -v ~/nrfis/backend/data_collection_system/var:/var --env DATABASE_URL=postgresql+psycopg2://postgres:<password>@127.0.0.1/nrfisdb web_server_image
```

Substitute in the database password, currently known to Lawrence Berry and Paul Fidler.

### To run tests locally:

```
export DATABASE_URL="sqlite:///./backend/web_server/tests/.test.db"
source venv/bin/activate  # Activate virtual environment
pytest backend/web_server
```

## App

The _App_ is a Javascript [React Native](http://reactnative.dev) iOS and Android app which allows users to visualise FBG sensor data on 3D models of the building and through graphical plots.

### To install:

```
cd frontend/app
npm install
```

### To run in development:

```
cd frontend/app
expo start
```

The app can then be tested on the iOS simulator on a Mac, or on a real iOS or Android device by installing the Expo app and following the QR link in the terminal and Expo web interface.
