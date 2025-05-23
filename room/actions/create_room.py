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
            "action": "room_created",  # ⚠️ Utiliser "action" au lieu de "type"
            "room": {
                "id": str(room_id),
                "_id": str(room_id),  # Pour compatibilité frontend
                "name": room_name,
                "created_by": username
            }
        }
        
        await ws.write_message(json.dumps(response))
        
        # Optionnel: Broadcaster à tous les clients connectés
        # await broadcast_to_all_clients(response)
        
    except Exception as e:
        print(f"Erreur création room: {str(e)}")  # Pour debug
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la création de la room : {str(e)}"
        }))