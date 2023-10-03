import asyncio
import logging

from app import mongodb
from app.handlers import enviar_email, notificar_webhook

PENDENTE = "PENDENTE"
ENVIADA = "ENVIADA"
FALHA_AO_ENVIAR = "FALHA_AO_ENVIAR"

def callback(task):
    result = task.result()[0]
    id_notificacao = task.result()[1]
    logging.info(f"Tentativa de envio da notificação ID={id_notificacao} finalizada. Resultado={result}")
    async def confirmacao_callback():
        status = ENVIADA if result else FALHA_AO_ENVIAR
        await mongodb.update_status(id_notificacao, status)
    asyncio.create_task(confirmacao_callback())

HANDLERS = {
    "email": enviar_email,
    "webhook": notificar_webhook
}

class NotificadorService():
    def __init__(self, rabbit):
        self.rabbit = rabbit

    async def processar_notificacao(self, id_notificacao):
        logging.info(f"Processamento notificação {id_notificacao}")
        notificacao = await mongodb.get_by_id(id_notificacao)
        handler = HANDLERS[notificacao["type"]]
        asyncio.create_task(handler(notificacao)).add_done_callback(callback)

    async def cadastrar_notificacao(self, notificacao):
        notificacao["status"] = PENDENTE
        id = await mongodb.save(notificacao)
        await self.rabbit.publish(id)

    async def listar_notificacoes(self):
        return await mongodb.list()