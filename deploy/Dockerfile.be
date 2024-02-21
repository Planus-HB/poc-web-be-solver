FROM python:3.9

WORKDIR /app

COPY be.py .

RUN pip install pika
RUN pip install websockets

CMD ["python", "be.py"]
