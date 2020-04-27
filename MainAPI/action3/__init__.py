import threading
from MainAPI.action3.consumer import Consumer

NUM_CONSUMERS = 2
QUEUE_ID = 'Action3_Q'
consumer_threads = []
for _ in range(NUM_CONSUMERS):
    thread = threading.Thread(target=Consumer(QUEUE_ID).start)
    thread.name = "Action3QueueWorker" + str(_ + 1)
    consumer_threads.append(thread)
    thread.start()
