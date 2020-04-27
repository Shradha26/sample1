import pika

RMQ_HOST = 'localhost'


class RMQConnection:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_HOST))
