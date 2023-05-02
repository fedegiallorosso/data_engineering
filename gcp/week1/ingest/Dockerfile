FROM python:3.9.1

WORKDIR /app

#RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

COPY . /app

ENTRYPOINT ["python", "ingest_data.py"]
