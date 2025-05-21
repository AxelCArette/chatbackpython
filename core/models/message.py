# Schéma Message
from datetime import datetime
from motor.motor_tornado import MotorClient
from config.settings import MONGO_URI # adapte selon ton fichier settings.py

client = MotorClient(MONGO_URI)
db = client["chat_db"]  # remplace "chat_db" par le nom de ta DB
messages_collection = db["messages"]



def create_message(content, msg_type, sender_id, room_id, parent_id=None):
    return {
        "content": content,
        "type": msg_type,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
        "sender_id": sender_id,
        "room_id": room_id,
        "parent_id": parent_id,
        "reactions": []
    }
