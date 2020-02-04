FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04

COPY ./web_server /app/app
COPY ./database_models /app/database_models

