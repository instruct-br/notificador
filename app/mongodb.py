from app.config import MONGO, MONGO_DATABASE
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

connection = AsyncIOMotorClient(MONGO)


async def connection_db():
    return connection


async def close_db():
    return connection.close()


async def get_db():
    return connection[MONGO_DATABASE]


async def server_info():
    return connection.server_info()

async def update_status(id_notificacao, status):
    session = await connection_db()
    db = await get_db()
    async with await session.start_session() as session:
        collection = db["generic"]
        await collection.update_one(
            {"_id": id_notificacao},
            {"$set": {"status": status }}
        )

async def save(notificacao):
    session = await connection_db()
    db = await get_db()
    async with await session.start_session() as session:
        collection = db["generic"]
        notification = await collection.insert_one(notificacao, session=session)
        return notification.inserted_id
    
async def get_by_id(id_notificacao):
    session = await connection_db()
    db = await get_db()
    async with await session.start_session() as session:
        collection = db["generic"]
        return await collection.find_one({"_id": ObjectId(id_notificacao)})

async def list():
    db = await get_db()
    collection = db["generic"]
    notificacoes = []
    async for document in collection.find({}):
        notificacoes.append({
            "id": str(document["_id"]),
            "status": document["status"],
            "titulo": document["titulo"]
        })
    return notificacoes