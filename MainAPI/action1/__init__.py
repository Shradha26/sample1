import threading
from MainAPI.action1.consumer import Consumer

NUM_CONSUMERS = 3
QUEUE_ID = 'Action1_Q'
consumer_threads = []
for _ in range(NUM_CONSUMERS):
    thread = threading.Thread(target=Consumer(QUEUE_ID).start)
    thread.name = "Action1QueueWorker" + str(_ + 1)
    consumer_threads.append(thread)
    thread.start()
