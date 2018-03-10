from python:3.6

EXPOSE 8000

ADD . /oser-backend

WORKDIR /oser-backend/oser_backend

# Debug only
RUN ls

RUN pip3 install -r ../requirements.txt
RUN pip3 install gunicorn

CMD sh ../start.sh
