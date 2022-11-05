FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r /code/requirements.txt --no-cache-dir
COPY . .
CMD python3 src/main.py
