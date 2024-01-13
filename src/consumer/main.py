import json
import logging
from pprint import pprint
from uuid import uuid4

import pika
import requests

pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(module)s/%(filename)s %(levelname)s:%(message)s",
)
logger = logging.getLevelName(__name__)


def callback(ch, method, properties, body):
    body = json.loads(body)
    body.update({"psp_id": str(uuid4())})
    response = requests.post(url=body.get("postback"), json=body)

    if response.status_code == 200:
        logging.info(
            f"Request Postback to {body.get('postback')} with body {str(body)}"
        )


if __name__ == "__main__":
    host = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(host)
    channel = connection.channel()
    channel.basic_consume(
        queue="create_charge_psp", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()
    logging.info("consumer running")
