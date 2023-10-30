FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y vim

COPY . .

CMD ["/app/start.sh"]
#CMD ["gunicorn", "photo_booking.wsgi:application", "--bind", "0:8000"]
