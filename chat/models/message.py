from datetime import datetime
from bson import ObjectId
from adapters.mongo.collections import messages_collection

class Message:
    def __init__(self, username, message, room_id, timestamp=None, _id=None):
        self._id = _id or ObjectId()
        self.username = username
        self.message = message
        self.room_id = room_id if isinstance(room_id, ObjectId) else ObjectId(room_id)
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "message": self.message,
            "room_id": self.room_id,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get("_id"),
            username=data["username"],
            message=data["message"],
            room_id=data["room_id"],
            timestamp=data.get("timestamp")
        )

    async def save(self):
        """Sauvegarde le message en base de données"""
        message_data = self.to_dict()
        result = await messages_collection.insert_one(message_data)
        self._id = result.inserted_id
        return self._id

    @classmethod
    async def find_by_room(cls, room_id, limit=100):
        """Récupère les messages d'une room"""
        if isinstance(room_id, str):
            room_id = ObjectId(room_id)
            
        cursor = messages_collection.find({"room_id": room_id}).sort("timestamp", 1).limit(limit)
        messages = []
        async for message_data in cursor:
            messages.append(cls.from_dict(message_data))
        return messages

    @classmethod
    async def find_all(cls, limit=100):
        """Récupère tous les messages"""
        cursor = messages_collection.find({}).sort("timestamp", 1).limit(limit)
        messages = []
        async for message_data in cursor:
            messages.append(cls.from_dict(message_data))
        return messages

    def serialize(self):
        """Sérialise le message pour JSON"""
        return {
            "_id": str(self._id),
            "username": self.username,
            "message": self.message,
            "room_id": str(self.room_id),
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }