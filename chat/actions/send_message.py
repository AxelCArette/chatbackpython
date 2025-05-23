import json
from chat.services.message_service import save_message

async def handle_send_message(data, ws):
    username = data.get("username")
    content = data.get("message")
    room_id = data.get("room_id")

    if not username or not content:
        await ws.write_message(json.dumps({
            "type": "error",
            "message": "Username et message requis"
        }))
        return

    if not room_id:
        await ws.write_message(json.dumps({
            "type": "error", 
            "message": "room_id requis"
        }))
        return

    try:
        # Sauvegarder le message
        saved_message = await save_message(username, content, room_id)
        
        # Préparer la réponse pour broadcast
        broadcast_data = {
            "action": "new_message",
            "username": username,
            "message": content,
            "room_id": room_id,
            "timestamp": saved_message["timestamp"]
        }
        
        # Broadcast à tous les clients connectés
        from websocket.chat_ws_handler import ChatWebSocketHandler
        await ChatWebSocketHandler.broadcast_to_all(broadcast_data)
        
    except Exception as e:
        print(f"Erreur send_message: {str(e)}")
        await ws.write_message(json.dumps({
            "type": "error",
            "message": f"Erreur lors de l'envoi du message: {str(e)}"
        }))