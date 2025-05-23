# room/actions/get_rooms.py
from room.services.room_service import get_all_rooms
import json

async def handle_get_rooms(data, ws):
    try:
        # Récupérer toutes les rooms depuis la base
        rooms_data = await get_all_rooms()  # ← Ça retourne déjà des dict avec to_dict()
        
        # Les rooms sont déjà converties en dict avec les string
        # Pas besoin de conversion supplémentaire
        
        # Répondre avec toutes les rooms
        response = {
            "type": "room_list",  # ← Changer "action" en "type" pour matcher le frontend
            "rooms": rooms_data
        }
        
        await ws.write_message(json.dumps(response))
        
    except Exception as e:
        print(f"Erreur récupération rooms: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la récupération des rooms : {str(e)}"
        }))