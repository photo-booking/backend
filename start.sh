#!/bin/sh
uwsgi -d --ini uwsgi.ini &
daphne -b 0.0.0.0 -p 8002 photo_booking.asgi:application
