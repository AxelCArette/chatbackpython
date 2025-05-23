import json
from chat.services.message_service import get_messages_by_room

async def handle_get_messages(data, ws):
    room_id = data.get("room_id")
    
    if not room_id:
        await ws.write_message(json.dumps({
            "type": "error",
            "message": "room_id requis"
        }))
        return

    try:
        messages = await get_messages_by_room(room_id)
        
        response = {
            "action": "room_messages",
            "room_id": room_id,
            "messages": messages
        }
        
        await ws.write_message(json.dumps(response))
        
    except Exception as e:
        print(f"Erreur get_messages: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de la récupération des messages: {str(e)}"
        }))