FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && pip3 install -r requirements.txt
COPY pnzsad/. .
COPY data .
CMD gunicorn pnzsad.wsgi:application --bind 0.0.0.0:8000
