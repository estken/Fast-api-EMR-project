from .conftest import get_session, admin_login
from db.room_model import ClientRoom
from db.equipment_model import ClientEquipment
from .seeder import seed_client, seed_client_center
from schemas.room_schema import EquipmentNameBase

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

def test_create_equipment_endpoint(get_session, client_instance, client_header, admin_details):
    get_session.query(ClientEquipment).delete()
    token = admin_login(get_session, client_instance, client_header, admin_details)
    gadget_data = {
        'equipment': "test equipment"
    }
    equip = get_session.query(ClientEquipment).all()
    assert len(equip) == 0
    response = client_instance.post("/equipment/create", headers={"Authorization": f"Bearer {token}"}, json= gadget_data)
    assert response.status_code == 201
    equipment = get_session.query(ClientEquipment).all()
    assert len(equipment) == 1
    first = get_session.query(ClientEquipment).first()
    assert first.equipment == "test equipment"
    assert first.slug is not None

def test_create_equipment_duplicate_endpoint(get_session, client_instance, client_header, admin_details):
    get_session.query(ClientEquipment).delete()
    token = admin_login(get_session, client_instance, client_header, admin_details)
    gadget_data = {
        'equipment': "test equipment"
    }
    equipment_1 = ClientEquipment(equipment ="test equipment", slug="test_slug")
    get_session.add(equipment_1)
    get_session.commit()
    equip = get_session.query(ClientEquipment).all()
    assert len(equip) == 1
    response = client_instance.post("/equipment/create", headers={"Authorization": f"Bearer {token}"}, json= gadget_data)
    assert response.status_code == 400
    assert response.json()['detail'] == "equipment test equipment already exists"
    assert response.json()['status'] == 0

def test_update_equipment_endpoint(get_session, client_instance, client_header, admin_details):
    get_session.query(ClientEquipment).delete()
    gadget_data2 = {
        'equipment': "test equipment2",
        'slug': 'test_slug'
    }
    equipment_1 = ClientEquipment(equipment ="test equipment", slug="test_slug")
    get_session.add(equipment_1)
    get_session.commit()
    equip = get_session.query(ClientEquipment).filter(ClientEquipment.slug=="test_slug").first()
    assert equip.equipment == "test equipment"
    token = admin_login(get_session, client_instance, client_header, admin_details)
    response = client_instance.patch("/equipment/update", headers={"Authorization": f"Bearer {token}"}, json= gadget_data2)
    assert response.status_code == 200
    assert response.json()['detail'] == "Equipment name changed to test equipment2"
    assert response.json()['status'] == 1
    equip2 = get_session.query(ClientEquipment).filter(ClientEquipment.slug=="test_slug").first()
    assert equip2.equipment == "test equipment2"

def test_lookup_single_equipment(get_session, client_instance, client_header, admin_details):
    get_session.query(ClientEquipment).delete()
    equipment_1 = ClientEquipment(equipment ="test equipment", slug="test_slug")
    get_session.add(equipment_1)
    get_session.commit()
    equip = get_session.query(ClientEquipment).filter(ClientEquipment.slug=="test_slug").first()
    assert equip.equipment == "test equipment"
    token = admin_login(get_session, client_instance, client_header, admin_details)
    response = client_instance.get("/equipment/view/test_slug", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['data']['equipment'] == "test equipment"

def test_list_all_equipment(get_session, client_instance, client_header, admin_details):
    get_session.query(ClientEquipment).delete()
    equipment_1 = ClientEquipment(equipment ="test equipment", slug="test_slug")
    get_session.add(equipment_1)
    equipment_2 = ClientEquipment(equipment ="test equipment2", slug="test_slug2")
    get_session.add(equipment_2)
    get_session.commit()
    equip = get_session.query(ClientEquipment).all()
    assert len(equip) == 2
    token = admin_login(get_session, client_instance, client_header, admin_details)
    response = client_instance.get("/equipment", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()['data']
    for gadget in data:
         assert gadget['equipment'] == "test equipment" or gadget['equipment'] == "test equipment2"
         assert gadget['slug'] == "test_slug" or gadget['slug'] == "test_slug2"

def test_delete_single_equipment(get_session, client_instance, client_header, admin_details):
    get_session.query(ClientEquipment).delete()
    equipment_1 = ClientEquipment(equipment ="test equipment", slug="test_slug")
    get_session.add(equipment_1)
    equipment_2 = ClientEquipment(equipment ="test equipment2", slug="test_slug2")
    get_session.add(equipment_2)
    get_session.commit()
    equip = get_session.query(ClientEquipment).all()
    assert len(equip) == 2
    token = admin_login(get_session, client_instance, client_header, admin_details)
    response = client_instance.delete("/equipment/delete/test_slug", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['detail'] == "Equipment test equipment delete successfully"
    assert response.json()['status'] == 1
    equipment = get_session.query(ClientEquipment).all()
    assert len(equipment) == 1
    for data in equipment:
        assert data.slug == 'test_slug2' 