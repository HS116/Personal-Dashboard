FROM python:3.10.2

WORKDIR /app
RUN pip install requests newsapi_python sqlalchemy psycopg2 
COPY financial.py ingesting.py

ENTRYPOINT ["python", "main.py"]