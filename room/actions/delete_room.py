from room.services.room_service import delete_room_by_id
import json

async def handle_delete_room(data, ws):
    room_id = data.get("room_id")
    username = data.get("username")

    if not room_id:
        await ws.write_message(json.dumps({
            "type": "error",
            "message": "L'ID de la room est requis."
        }))
        return

    try:
        # Supprimer la room de la base
        deleted = await delete_room_by_id(room_id)
        
        if deleted:
            # Répondre avec la room supprimée
            response = {
                "type": "room_deleted",
                "room_id": room_id
            }
            
            # Broadcaster à tous les clients connectés
            await ws.broadcast_to_all(response)
        else:
            await ws.write_message(json.dumps({
                "type": "error",
                "message": "Room non trouvée."
            }))
        
    except Exception as e:
        print(f"Erreur suppression room: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la suppression de la room : {str(e)}"
        }))