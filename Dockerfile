from python:3.6
EXPOSE 8000
ADD . /oser-backend
RUN pip3 install -r oser-backend/requirements.txt
WORKDIR /oser-backend/oser_backend
CMD python3 manage.py runserver 0.0.0.0:8000
