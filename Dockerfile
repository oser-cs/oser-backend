from python:3.6

EXPOSE 8000

ADD . /oser-backend

RUN pip3 install -r oser-backend/requirements.txt
RUN pip3 install gunicorn

WORKDIR /oser-backend/oser_backend

# Collect static files
RUN python3 manage.py collectstatic

# Initialize database
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Initialize admin users
RUN python3 manage.py initadmin

CMD sh ../start.sh
