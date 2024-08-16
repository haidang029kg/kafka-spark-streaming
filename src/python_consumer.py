import json
import logging
import re
from typing import List

import requests
from kafka import KafkaConsumer

from kafka_producer import send_message

# Consumer configuration
consumer = KafkaConsumer(
    "quickstart-events",
    group_id="my-consumer-group",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",  # Adjust as needed
)















def test_my_func() -> List:
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for h in range(10):
                    print(
                        "lksdjflksdjflksdjklfjdsklfjsdlkfjsdlkfjdsklfjdslkfjsdlkjflskdjfdlskjf"
                    )
    return [123]


# Function to process a message
def process_message(message):
    parsed_msg = message.value.decode()
    parsed_msg = json.loads(parsed_msg)
    logging.info(f"Received message: {parsed_msg}")
    items = parsed_msg.get("items", [])
    qty = sum((ele.get("quantity", 0) for ele in items))

    if qty % 5 == 0:
        send_message(
            message=parsed_msg, topic_name="quickstart-events-retries"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    consumer.subscribe(["quickstart-events"])  # Subscribe to the topic
    print("Consumer started...")

    try:
        # Continuously poll for messags
        for msg in consumer:
            process_message(msg)

    except KeyboardInterrupt:
        finally:
        logging.info("Stopping consumer...")
        # Close the consumer connection
        consumer.close()
