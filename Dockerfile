from python:3.6

EXPOSE 8000
ENV PYTHONUNBUFFERED=0

ADD . /oser-backend

WORKDIR /oser-backend/oser_backend

# Install dependencies
RUN pip3 install -r ../requirements.txt
RUN pip3 install gunicorn

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Setup database
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py initadmin

RUN echo "Content of oser-backend/ directory:"; ls ..
RUN echo "Content of oser_backend/ directory:"; ls

CMD sh ../start.sh
