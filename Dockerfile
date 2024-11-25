# to build the docker image run
# sudo docker build -t gamesite-image .
# To run gamesite in a container run
# sudo docker run --name gamesite -p 5000:5000 gamesite-image

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]