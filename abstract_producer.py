from abc import ABC, abstractmethod
from rmq_connection import RMQConnection


class AbstractProducer(ABC):
    def __init__(self):
        self.connection = RMQConnection().connection
        self.channel = self.connection.channel()

    @abstractmethod
    def publish(self, msg, key):
        return

    def shutdown(self):
        self.connection.close()