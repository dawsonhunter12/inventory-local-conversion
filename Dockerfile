FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Use the shell form of CMD to allow variable expansion
CMD gunicorn --bind 0.0.0.0:$PORT app:app
