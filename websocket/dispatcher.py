import importlib
from chat.actions.send_message import handle_send_message
from chat.actions.get_messages import handle_get_messages  
from room.actions.create_room import handle_create_room
from room.actions.get_rooms import handle_get_rooms
from room.actions.delete_room import handle_delete_room

# Dictionnaire avec les fonctions directement (pas des strings)
chat_actions = {
    "send_message": handle_send_message,
    "get_messages": handle_get_messages,
    "create_room": handle_create_room,
    "get_rooms": handle_get_rooms,
    "delete_room": handle_delete_room
}

async def dispatch_action(action, data, ws):
    """Dispatcher pour les actions WebSocket"""
    if action in chat_actions:
        handler_function = chat_actions[action]
        try:
            await handler_function(data, ws)
        except Exception as e:
            print(f"Erreur dans action {action}: {e}")
            await ws.write_message({
                "type": "error",
                "message": f"Erreur lors de l'exécution de {action}"
            })
    else:
        await ws.write_message({
            "type": "error", 
            "message": f"Action inconnue: {action}"
        })