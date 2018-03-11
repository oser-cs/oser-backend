from python:3.6

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

ADD . /oser-backend

WORKDIR oser-backend/oser_backend

RUN ls

# Install dependencies
RUN pip3 install -r ../requirements.txt
RUN pip3 install gunicorn

CMD sh ../start.sh
