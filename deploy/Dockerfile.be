FROM python:3.9

WORKDIR /app

COPY src/be.py .

RUN pip install pika
RUN pip install websockets

CMD ["python", "be.py"]
