# Dockerfile, Image, Container
FROM python:3.8
COPY . .
ADD wikipedia_main.py .
RUN pip install requests
RUN pip install jproperties
RUN pip install mysql-client
RUN pip install mysql-connector-python

CMD ["python","./wikipedia_main.py"]
