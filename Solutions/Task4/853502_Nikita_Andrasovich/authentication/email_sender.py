from multiprocessing import Process, Queue
from django.core.mail import EmailMessage
import time
import queue
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

IS_RUNNING = False
message_queue = Queue()


def send(subject, message, to):
    message_queue.put(EmailMessage(subject, message, to=[to]))
    logger.info("Added message for " + to + " into queue")

    if not IS_RUNNING:
        _start()


def _start():
    for _ in range(4):
        process = Process(target=_process_message_queue, args=())
        process.daemon = True
        process.start()

    logger.info("Started message sender service")
    global IS_RUNNING
    IS_RUNNING = True


def _process_message_queue():
    while True:
        try:
            message = message_queue.get_nowait()
        except queue.Empty:
            time.sleep(1)
            continue
        else:
            logger.info("Email sender service sending message...")
            message.send()
