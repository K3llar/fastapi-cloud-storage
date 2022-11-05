FROM python:3.10-slim

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r /code/requirements.txt
COPY . .
CMD python3 src/main.py
