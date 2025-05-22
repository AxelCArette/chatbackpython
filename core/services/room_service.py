from adapters.mongo.collections import rooms_collection
from datetime import datetime
from bson import ObjectId

async def save_room(name: str, users: list):
    result = await rooms_collection.insert_one({
        "name": name,
        "users": users,
        "createdAt": datetime.utcnow()
    })
    return str(result.inserted_id)

async def get_all_rooms():
    cursor = rooms_collection.find().sort("createdAt", -1)
    return [
        {
            "_id": str(doc["_id"]),
            "name": doc["name"],
            "users": doc.get("users", []),
            "createdAt": doc.get("createdAt")
        }
        async for doc in cursor
    ]

async def delete_room_by_id(room_id: str):
    result = await rooms_collection.delete_one({"_id": ObjectId(room_id)})
    return result.deleted_count