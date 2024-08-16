import time

import schedule

from src.kafka_producer import send_message
from src.utils import generate_orders


def gen_func():
    print("Generate fake orders")
    orders = generate_orders(10)
    for order in orders:
        print(order)
        send_message(order)


if __name__ == "__main__":

    schedule.every(100).seconds.do(gen_func)

    while True:

        schedule.run_pending()
        time.sleep(1)
