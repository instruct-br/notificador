from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from app.service import NotificadorService
from app.rabbitmq import rabbit

service = NotificadorService(rabbit)
router = APIRouter()


class NotificacaoPayload(BaseModel):
    type: str
    email: str = None
    webhook: str = None
    titulo: str
    mensagem: str

def validate(payload: NotificacaoPayload):
    if payload.type not in ["email", "webhook"]:
        raise HTTPException(status_code=400, detail="O campo 'type' deve ser 'email' ou 'webhook'")
    
    if payload.type == "email" and not payload.email:
        raise HTTPException(status_code=400, detail="O campo 'email' é obrigatório para 'type' igual a 'email'")
    
    if payload.type == "webhook" and not payload.webhook:
        raise HTTPException(status_code=400, detail="O campo 'webhook' é obrigatório para 'type' igual a 'webhook'")

@router.post("/notificacoes", status_code=HTTP_201_CREATED)
async def cadastrar_notificacao(payload: NotificacaoPayload):
    validate(payload)
    await service.cadastrar_notificacao(payload.__dict__)
    return {"result": "Notificação cadastrada com sucesso."}

@router.get("/notificacoes")
async def listar_notificacoes():
    return await service.listar_notificacoes()
