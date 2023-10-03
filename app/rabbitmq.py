import asyncio
import json
import logging
import sys
import traceback

from aio_pika import IncomingMessage, Message, connect_robust
from app.config import QUEUE_NAME, RABBITMQ_URI
from app.service import NotificadorService


class RabbitMQPublisher:
    def __init__(self, uri) -> None:
        self.uri = uri
        self.service = NotificadorService(self)

    async def connect(self):
        self.connection = await connect_robust(self.uri)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(QUEUE_NAME, durable=True)
        self.exchange = self.channel.default_exchange

    async def setup(self):
        await self.queue.consume(self.callback)


    async def publish(self, message):
        await self.exchange.publish(
            Message(json.dumps(message, default=str).encode()), routing_key=QUEUE_NAME
        )

    async def callback(self, message: IncomingMessage):
        async with message.process(requeue=True, ignore_processed=True):
            try:
                details = json.loads(message.body.decode("utf-8"))
                asyncio.create_task(self.service.processar_notificacao(details))
                await message.ack()
            except Exception as e:
                await message.ack()
                traceback.print_exc()
                logging.error("Erro ao processar mensagem: %s", str(e))
    
    async def disconnect(self):
        await self.connection.close()

    async def is_connected(self):
        if self.connection.is_closed:
            raise Exception("connection error rabbitmq")


rabbit = RabbitMQPublisher(RABBITMQ_URI)


async def setup_rbmq():
    try:
        await rabbit.connect()
        await rabbit.setup()
    except Exception as e:
        logging.error(" ERR : %s", str(e))
        sys.exit(1)