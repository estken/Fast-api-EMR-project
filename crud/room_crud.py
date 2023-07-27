from response_handler import error_response as exceptions
from response_handler import success_response
from db.equipment_model import ClientEquipment
from db.client_model import Client
from schemas.room_schema import RoomBase, EquipmentSlugBase, EquipmentNameBase, EquipmentCreateBase

def create_client_equipment(db, equipment: EquipmentCreateBase):
    try:
        gadget = ClientEquipment.lookup_eqipment_by_name(db, equipment.equipment)
        if gadget:
            return exceptions.bad_request_error(f"equipment {equipment.equipment} already exists")
        ClientEquipment.insert_equipment(db, equipment.__dict__)
        db.commit()
        return success_response.success_message([], f"Equipment {equipment.equipment} was successfully created", 201)
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    

def update_client_equipment(db, equipment: EquipmentNameBase):
    try:
        gadget = ClientEquipment.lookup_eqipment_by_slug(db, equipment.slug)
        if gadget is None:
            return exceptions.bad_request_error("Equipment not found")
        gadget.equipment = equipment.equipment
        db.add(gadget)
        db.commit()
        return success_response.success_message([], f"Equipment name changed to {equipment.equipment}", 200)
    except Exception as e:
        return exceptions.server_error(detail=str(e))

# remeber to delete all rooms equipment assigned to
def delete_client_equipment(db, data: EquipmentSlugBase):
    try:
        gadget = ClientEquipment.lookup_eqipment_by_slug(db, data.slug)
        if gadget is None:
            return exceptions.bad_request_error("Equipment not found")
        gadget_data = gadget.__dict__
        db.delete(gadget)
        db.commit()

        return success_response.success_message(gadget_data, f"Equipment {gadget.equipment} delete successfully", 200)
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    

def list_client_equipment(db):
    try:
        gadget = ClientEquipment.get_all_client_equipment(db)
        return success_response.success_message(gadget)
    except Exception as e:
        return exceptions.server_error(detail=str(e))

def get_single_equipment(db, data: EquipmentSlugBase):
    try:
        gadget = ClientEquipment.lookup_eqipment_by_slug(db, data.slug)
        return success_response.success_message(gadget)
    except Exception as e:
        return exceptions.server_error(detail=str(e))   