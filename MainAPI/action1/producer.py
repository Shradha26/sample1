from abstract_producer import AbstractProducer


class Producer(AbstractProducer):
    def __init__(self):
        super().__init__()

    def publish(self, resource_id, key):
        self.channel.basic_publish(exchange='', routing_key=key, body=resource_id)
