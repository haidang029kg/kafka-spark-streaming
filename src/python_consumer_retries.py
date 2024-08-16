import json
import logging

from kafka import KafkaConsumer

from kafka_producer import send_message

# Consumer configuration
consumer = KafkaConsumer(
    "quickstart-events-retries",
    group_id="my-consumer-group",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",  # Adjust as needed
)


# Function to process a message
def process_message(message):
    print(message)
    parsed_msg = message.value.decode()
    logging.info(f"Received message: {parsed_msg}")
    parsed_msg = json.loads(parsed_msg)
    items = parsed_msg.get("items", [])

    if len(items) % 2 == 0:
        send_message(message=parsed_msg, topic_name="quickstart-events-DLQ")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    consumer.subscribe(["quickstart-events-retries"])  # Subscribe to the topic
    print("Consumer started...")

    try:
        # Continuously poll for messages
        for msg in consumer:
            process_message(msg)

    except KeyboardInterrupt:
        logging.info("Stopping consumer...")
    finally:
        # Close the consumer connection
        consumer.close()
