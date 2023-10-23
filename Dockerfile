
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y vim

COPY . .

CMD ["gunicorn", "photo_booking.wsgi:application", "--bind", "0:8000"]