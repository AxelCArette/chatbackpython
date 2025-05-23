# room/models/room.py - Version complète
from datetime import datetime
from bson import ObjectId
from adapters.mongo.collections import rooms_collection

class Room:
    def __init__(self, name, created_by=None, created_at=None, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.created_by = created_by
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),  # Convertir ObjectId en string
            "id": str(self._id),   # Alias pour compatibilité frontend
            "name": self.name,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None  # Convertir datetime
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get("_id"),
            name=data["name"],
            created_by=data.get("created_by"),
            created_at=data.get("created_at")
        )

    async def save(self):
        """Sauvegarde la room en base de données"""
        room_data = self.to_dict()
        # Remettre l'ObjectId pour MongoDB
        room_data["_id"] = self._id
        room_data["created_at"] = self.created_at  # Remettre datetime pour MongoDB
        del room_data["id"]  # Supprimer l'alias
        
        result = await rooms_collection.insert_one(room_data)
        self._id = result.inserted_id
        return self._id

    @classmethod
    async def find_all(cls):
        """Récupère toutes les rooms"""
        cursor = rooms_collection.find({})
        rooms = []
        async for room_data in cursor:
            rooms.append(cls.from_dict(room_data))
        return rooms

    @classmethod
    async def find_by_id(cls, room_id):
        """Trouve une room par son ID"""
        if isinstance(room_id, str):
            room_id = ObjectId(room_id)
        
        room_data = await rooms_collection.find_one({"_id": room_id})
        if room_data:
            return cls.from_dict(room_data)
        return None

    @classmethod
    async def find_by_name(cls, name):
        """Trouve une room par son nom"""
        room_data = await rooms_collection.find_one({"name": name})
        if room_data:
            return cls.from_dict(room_data)
        return None

    async def delete(self):
        """Supprime la room"""
        await rooms_collection.delete_one({"_id": self._id})
        return True