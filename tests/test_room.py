from .conftest import get_session
from db.room_model import ClientRoom
from .seeder import seed_client, seed_client_center

def get_first_room_by_name(get_session, center_id: int, room: str):
        return get_session.query(ClientRoom).filter(ClientRoom.center_id == center_id, ClientRoom.name == room).first()


def test_create_room(get_session):
    seed_client(get_session)
    seed_client_center(get_session)
    room_data = {
        'name': 'room_1',
        'description': 'test data',
        'center_id': 1
    }
    rooms = get_session.query(ClientRoom).all()
    assert len(rooms) == 0
    ClientRoom.insert_room(get_session, room_data)
    get_session.commit()
    new_rooms = get_session.query(ClientRoom).all()
    assert len(new_rooms) == 1
    room = get_first_room_by_name(get_session, 1, 'room_1')
    assert room.description == 'test data'
    assert room.status == True
    assert room.slug is not None