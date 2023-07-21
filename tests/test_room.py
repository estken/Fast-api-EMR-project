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

def test_get_first_room_uuid(get_session):
    seed_client(get_session)
    seed_client_center(get_session)
    room_1 = ClientRoom(name="room_2", description='test data2', center_id =1, slug='slug2')
    get_session.add(room_1)
    get_session.commit()
    room = ClientRoom.get_first_room(get_session, 1, 'slug2')
    assert room.name == 'room_2'

def test_get_all_center_rooms(get_session):
    get_session.query(ClientRoom).delete()
    seed_client(get_session)
    seed_client_center(get_session)
    room_3 = ClientRoom(name="room_3", description='test data3', center_id =1, slug='slug3')
    get_session.add(room_3)
    room_4 = ClientRoom(name="room_4", description='test data4', center_id =1, slug='slug4')
    get_session.add(room_4)
    room_5 = ClientRoom(name="room_5", description='test data5', center_id =2, slug='slug5')
    get_session.add(room_5) #different center id
    get_session.commit()
    rooms = ClientRoom.get_center_rooms(get_session, 1)
    assert len(rooms) == 2
    for data in rooms:
         assert data.name !='room_5'

def test_get_all_center_rooms_by_status(get_session):
    get_session.query(ClientRoom).delete()
    seed_client(get_session)
    seed_client_center(get_session)
    room_3 = ClientRoom(name="room_3", description='test data3', center_id =1, slug='slug3')
    get_session.add(room_3)
    room_4 = ClientRoom(name="room_4", description='test data4', center_id =1, slug='slug4')
    get_session.add(room_4)
    room_5 = ClientRoom(name="room_5", description='test data5', center_id =1, slug='slug5', status =False)
    get_session.add(room_5) #different status
    get_session.commit()
    rooms = ClientRoom.get_center_rooms_by_status(get_session, 1, 1)
    assert len(rooms) == 2
    for data in rooms:
         assert data.name !='room_5'
