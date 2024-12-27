from threading import Thread
from kombu import Connection, Exchange, Queue
from core.tasks import process_notification

      
class MultiBrokerConsumer:
    def __init__(self, broker_configs):
        self.broker_configs = broker_configs

    def consume_from_broker(self, broker_config):
        print(f"Starting to listen to broker: {broker_config['url']}")
        connection = Connection(broker_config['url'])
        exchange = Exchange(broker_config['exchange']['name'], type=broker_config['exchange']['type'])
        
        queues = [
            Queue(queue_config['name'], exchange, routing_key=queue_config['routing_key'])
            for queue_config in broker_config['queues']
        ]
        
        with connection:
            consumer = connection.Consumer(queues, callbacks=[self.process_message])
            print(f"Consuming messages from {broker_config['url']}...")
            consumer.consume()  
            connection.drain_events()

    def consume(self):
        threads = []
        
        for broker_config in self.broker_configs:
            thread = Thread(target=self.consume_from_broker, args=(broker_config,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

    @staticmethod
    def process_message(body, message):
        print(f"Received message: {message}")
        print(f"Message body: {body}")
        process_notification.delay(body)
        message.ack()

