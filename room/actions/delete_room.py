# back/room/actions/delete_room.py

import json
from room.services.room_service import delete_room_by_id
from room.utils.broadcast import broadcast_room_deleted  # 🚫 plus d'import circulaire

async def handle_delete_room(data, ws):
    room_id = data.get("room_id")

    if not room_id:
        await ws.write_message(json.dumps({
            "type": "error",
            "message": "L'ID de la room est requis."
        }))
        return

    try:
        deleted = await delete_room_by_id(room_id)

        if deleted:
            await ws.write_message(json.dumps({
                "action": "room_deleted",
                "room_id": room_id
            }))

            await broadcast_room_deleted(room_id)  # ✅ moved here

        else:
            await ws.write_message(json.dumps({
                "type": "error",
                "message": "La room n'existe pas ou n'a pas pu être supprimée."
            }))

    except Exception as e:
        print(f"[WS] Erreur suppression room: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la suppression de la room : {str(e)}"
        }))
