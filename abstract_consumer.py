from abc import ABC, abstractmethod
from rmq_connection import RMQConnection


class AbstractConsumer(ABC):
    def __init__(self, queue_id):
        self.connection = RMQConnection().connection
        self.channel = self.connection.channel()
        self.queue_id = queue_id

    def start(self):
        def callback(ch, method, properties, body):
            self.consume(body.decode("utf-8"))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue=self.queue_id, on_message_callback=callback)
        print('Starting consumer for ' + str(self.queue_id))
        self.channel.start_consuming()

    @abstractmethod
    def consume(self, body):
        return

    def shutdown(self):
        self.connection.close()