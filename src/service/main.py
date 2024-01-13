import json
import logging
from typing import List, Union

import pika
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(module)s/%(filename)s %(levelname)s:%(message)s",
)
logger = logging.getLevelName(__name__)

app = FastAPI()


class Customer(BaseModel):
    name: str = Field(..., min_length=1)


class Items(BaseModel):
    value: float
    quantity: int


class Charge(BaseModel):
    card_token: str = Field(..., min_length=1)
    items: List[Items]
    customer: Customer


class Chaged(BaseModel):
    psp_id: str = Field(..., min_length=1)
    card_token: str = Field(..., min_length=1)
    items: List[Items]
    customer: Customer


@app.post("/charge")
def create_charge(body: Charge):
    body = body.model_dump()
    body.update({"status": "PENDING", "postback": "http://127.0.0.1:5000/charged"})
    connect_amqp(body)
    return body


@app.post("/charged")
def recive_charge(body: Chaged):
    print(body.model_dump())


def connect_amqp(data):
    host = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(host)
    channel = connection.channel()
    channel.queue_declare(queue="create_charge_psp")
    channel.basic_publish(
        exchange="", routing_key="create_charge_psp", body=json.dumps(data)
    )
    connection.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
