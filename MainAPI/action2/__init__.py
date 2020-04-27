import threading
from MainAPI.action2.consumer import Consumer

NUM_CONSUMERS = 5
QUEUE_ID = 'Action2_Q'
consumer_threads = []
for _ in range(NUM_CONSUMERS):
    thread = threading.Thread(target=Consumer(QUEUE_ID).start)
    thread.name = "Action2QueueWorker" + str(_ + 1)
    consumer_threads.append(thread)
    thread.start()
