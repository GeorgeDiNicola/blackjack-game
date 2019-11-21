FROM python:3.6

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /application
WORKDIR /application

EXPOSE 5000

CMD ["python3", "application/main.py"]