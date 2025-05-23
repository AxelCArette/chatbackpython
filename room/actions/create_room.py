# room/actions/create_room.py - Correction
from room.services.room_service import create_room_in_db
import json

async def handle_create_room(data, ws):
    room_name = data.get("room_name")
    username = data.get("username")

    if not room_name:
        await ws.write_message(json.dumps({
            "type": "error",
            "message": "Le nom de la room est requis."
        }))
        return

    try:
        # Créer la room en base avec le username
        room_id = await create_room_in_db(room_name, created_by=username)
        
        # Répondre avec la room créée
        response = {
            "type": "room_created",  # ← Changer "action" en "type"
            "room": {
                "id": str(room_id),
                "_id": str(room_id),
                "name": room_name,
                "created_by": username
            }
        }
        
        await ws.write_message(json.dumps(response))
        
        # Broadcaster à tous les clients connectés
        await ws.broadcast_to_all(response)
        
    except Exception as e:
        print(f"Erreur création room: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la création de la room : {str(e)}"
        }))