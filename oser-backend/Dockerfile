from python:3.6-alpine

# postgresql dependencies on Linux Alpine
RUN apk update && apk add build-base postgresql-dev libffi-dev
# pillow dependencies on Linux Alpine
RUN apk add --no-cache jpeg-dev zlib-dev

ENV PYTHONUNBUFFERED=1
# set port to 8000 if not defined (e.g. in development)
ENV PORT=${PORT:-8000}

ADD . /oser-backend
WORKDIR /oser-backend/oser_backend

# Install dependencies
RUN echo "Installing dependencies..." && pip3 install -r ../requirements.txt && pip3 install gunicorn

# Migrations are not run here
# They should be run once the container have started

RUN echo "Collecting static files..." && python manage.py collectstatic --noinput

# Run app as non-root user
RUN adduser -D user
USER user

CMD sh ../start.sh
