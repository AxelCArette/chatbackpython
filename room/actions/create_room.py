# room/actions/create_room.py
import json
from datetime import datetime
from room.services.room_service import create_room_in_db

# On vire le broadcast direct ici pour éviter le circular import
# -> Ce sera le handler qui fera le broadcast

async def handle_create_room(data, ws):
    room_name = data.get("room_name")
    username = data.get("username")

    if not room_name:
        await ws.write_message(json.dumps({
            "type": "error",
            "message": "Le nom de la room est requis."
        }))
        return None

    try:
        # Créer la room en base avec le username
        room_id = await create_room_in_db(room_name, created_by=username)

        # Préparer et retourner l'objet room
        new_room = {
            "id": str(room_id),
            "_id": str(room_id),  # Pour compatibilité frontend
            "name": room_name,
            "created_by": username,
            "created_at": datetime.utcnow().isoformat()
        }

        return new_room

    except Exception as e:
        print(f"Erreur création room: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la création de la room : {str(e)}"
        }))
        return None
