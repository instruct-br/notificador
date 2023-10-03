import asyncio
from fastapi import FastAPI
import logging

from app import mongodb, routes
from app.rabbitmq import setup_rbmq

logging.getLogger().setLevel(logging.INFO)
app = FastAPI(title="Notificador")
app.include_router(routes.router)

@app.on_event("startup")
async def startup():
    await mongodb.connection_db()
    asyncio.create_task(setup_rbmq())
    logging.info("Starting up...")
