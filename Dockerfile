from python:3.6

EXPOSE 8000

ADD . /oser-backend

RUN pip3 install -r oser-backend/requirements.txt
RUN pip3 install gunicorn

WORKDIR /oser-backend/oser_backend

CMD sh ../start.sh
