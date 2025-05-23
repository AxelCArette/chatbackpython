from chat.models.message import Message
from bson import ObjectId

async def save_message(username: str, message: str, room_id: str):
    """
    Sauvegarde un nouveau message dans la base de données
    """
    try:
        # Créer le message
        msg = Message(username=username, message=message, room_id=room_id)
        message_id = await msg.save()
        
        # Retourner le message sérialisé
        return msg.serialize()
    except Exception as e:
        raise Exception(f"Erreur lors de la sauvegarde du message: {str(e)}")

async def get_messages_by_room(room_id: str, limit: int = 100):
    """
    Récupère tous les messages d'une room
    """
    try:
        messages = await Message.find_by_room(room_id, limit)
        return [msg.serialize() for msg in messages]
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des messages: {str(e)}")

async def get_all_messages(limit: int = 100):
    """
    Récupère tous les messages (pour debug ou admin)
    """
    try:
        messages = await Message.find_all(limit)
        return [msg.serialize() for msg in messages]
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des messages: {str(e)}")

# Fonction legacy pour compatibilité
def serialize_message(message: dict) -> dict:
    """
    Fonction utilitaire pour sérialiser un message (legacy)
    """
    return {
        "_id": str(message.get("_id")),
        "username": message.get("username"),
        "message": message.get("message"),
        "room_id": str(message.get("room_id")) if isinstance(message.get("room_id"), ObjectId) else message.get("room_id"),
        "timestamp": message.get("timestamp").isoformat() if message.get("timestamp") else None,
    }