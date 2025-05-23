from room.services.room_service import get_all_rooms
import json
from datetime import datetime


async def handle_get_rooms(data, ws):
    try:
        rooms = await get_all_rooms()
        
        rooms_for_json = []
        for room in rooms:
            room_dict = room.copy()
            room_dict["_id"] = str(room_dict["_id"])
            room_dict["id"] = str(room_dict["_id"])
            
            # Convertir les datetime en string ISO
            for key, value in room_dict.items():
                if isinstance(value, datetime):
                    room_dict[key] = value.isoformat()
            
            rooms_for_json.append(room_dict)

        response = {
            "action": "rooms_list",
            "rooms": rooms_for_json
        }
        
        await ws.write_message(json.dumps(response))

    except Exception as e:
        print(f"Erreur get_rooms: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la récupération des rooms : {str(e)}"
        }))
