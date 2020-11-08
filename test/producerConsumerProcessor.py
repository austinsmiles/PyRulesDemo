import logging
import queue
import threading
import concurrent.futures
import time

some_global_variable="some_global_value"

class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__()

    def get_message(self, name):
        value = self.get()
        return value

    def set_message(self, value, name):
        self.put(value)


def producer(pipeline, event, name):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        for x in range(50):
            if pipeline.qsize() < 10:
                pipeline.set_message(x, "Producer")
                logging.info(f"Producer-{name} adding message: {x} [queue size: {pipeline.qsize()}]")
            else:
                logging.info("Queue is full, sleeping for 1s")
                logging.info(f"global (fm producer)- {some_global_variable}")
                time.sleep(1)

    logging.info(f"Producer-{name} received EXIT event. Exiting")


def consumer(pipeline, event, name):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info(f"Consumer-{name} consuming message: {message} [queue size: {pipeline.qsize()}]")
        logging.info(f"global (fm consumer)- {some_global_variable}")
        time.sleep(3)
    logging.info(f"Consumer-{name} received EXIT event. Exiting")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(producer, pipeline, event, 1)
        executor.submit(consumer, pipeline, event, 1)
        executor.submit(consumer, pipeline, event, 2)
        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()