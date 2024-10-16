FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use the shell form to allow environment variable expansion
CMD gunicorn --bind 0.0.0.0:$PORT app:app
