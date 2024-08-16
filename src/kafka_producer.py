import json
from typing import Union

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])


TOPIC = "quickstart-events"


def send_message(
    message: Union[dict, str], topic_name: Union[str, None] = None
):
    if not topic_name:
        topic_name = TOPIC

    if isinstance(message, dict):
        value = json.dumps(message).encode("utf-8")
    else:
        value = message.encode("utf-8")

    producer.send(topic=topic_name, value=value)
    producer.flush()
