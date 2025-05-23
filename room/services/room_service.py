from room.models.room import Room

async def create_room_in_db(room_name, created_by=None):
    """
    Crée une nouvelle room dans la base de données
    """
    # Vérifier si une room avec ce nom existe déjà
    existing_room = await Room.find_by_name(room_name)
    if existing_room:
        raise Exception(f"Une room avec le nom '{room_name}' existe déjà")
    
    # Créer la nouvelle room
    room = Room(name=room_name, created_by=created_by)
    room_id = await room.save()
    
    return room_id

async def get_all_rooms():
    """
    Récupère toutes les rooms
    """
    rooms = await Room.find_all()
    return [room.to_dict() for room in rooms]

async def get_room_by_id(room_id):
    """
    Récupère une room par son ID
    """
    room = await Room.find_by_id(room_id)
    return room.to_dict() if room else None

async def delete_room_by_id(room_id):
    """
    Supprime une room par son ID
    """
    room = await Room.find_by_id(room_id)
    if room:
        await room.delete()
        return True
    return False