# websocket/broadcast.py
import json

clients = set()

async def broadcast_to_clients(payload: dict):
    for client in clients:
        await client.write_message(json.dumps(payload))


clients = set()

async def broadcast_rooms(rooms):
    import json
    message = json.dumps({"action": "rooms_list", "rooms": rooms})
    for client in clients:
        await client.write_message(message)
