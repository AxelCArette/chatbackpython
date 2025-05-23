# back/room/utils/broadcast.py

import json
from websocket.room_handler import RoomWebSocketHandler

async def broadcast_room_deleted(room_id):
    await RoomWebSocketHandler.broadcast_to_all({
        "action": "room_deleted",
        "room_id": room_id
    })
