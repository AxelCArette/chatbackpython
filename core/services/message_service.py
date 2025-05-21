from adapters.mongo.collections import messages_collection
from datetime import datetime
from bson import ObjectId  # ✅ Pour check les types Mongo
from core.models.message import messages_collection

# 🔧 Sérialiseur simple
def serialize_message(message: dict) -> dict:
    return {
        "_id": str(message["_id"]) if "_id" in message else None,
        "username": message["username"],
        "message": message["message"],
        "room_id": str(message["room_id"]) if isinstance(message["room_id"], ObjectId) else message["room_id"],
        "timestamp": message["timestamp"].isoformat() if "timestamp" in message else None,
    }

async def save_message(username: str, message: str, room_id: str = "general"):
    await messages_collection.insert_one({
        "username": username,
        "message": message,
        "room_id": room_id,
        "timestamp": datetime.utcnow()
    })

async def get_all_messages():
    cursor = messages_collection.find().sort("timestamp", 1)
    return [serialize_message(doc) async for doc in cursor]  # ✅ On serialize ici aussi

async def get_messages_by_room(room_id: str):
    cursor = messages_collection.find({"room_id": room_id}).sort("timestamp", 1)
    return [serialize_message(msg) async for msg in cursor]  # ✅ Serialize les messages
