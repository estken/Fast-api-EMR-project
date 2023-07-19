# from .conftest import get_session
# import sys
# sys.path.append("..")
# from db import client_model as models
# from schema import (
#     ClientCenterSchema,
#     UpdateClientCenterSchema
# )
# from .seeder import( 
#     seed_client,
#     seed_client_center
# )
# import uuid

# def test_create_client_center(get_session):
#     # seed the client.
#     seed_client(get_session)
#     # set up the client center data
#     center_data = {
#         'client_id': 1,
#         'center': 'Center 1'
#     }
    
#     retrieve_centers = models.ClientCenter.get_all_center(get_session)
#     assert len(retrieve_centers) == 0
#     # create the new center.
#     created_center = models.ClientCenter.create_center(center_data)
#     get_session.add(created_center)
#     get_session.commit()
#     # 
#     retrieve_centers = models.ClientCenter.get_all_center(get_session)
#     assert len(retrieve_centers) == 1
    
# def test_view_client_centers(get_session):
#     # seed the client and client center.
#     seed_client(get_session)
#     seed_client_center(get_session)
#     # view all client centers.
#     retrieve_center = models.ClientCenter.get_all_client_center(get_session, 1)
#     assert len(retrieve_center) == 3
    
# def test_update_client_center(get_session):
#     # seed the client and client center.
#     seed_client(get_session)
#     seed_client_center(get_session)
#     # updated_data
#     update_data = {
#         'status': False,
#         'center': 'center 7'
#     }
#     # get the client center.
#     get_center = models.ClientCenter.get_center_by_id(get_session, 1)
#     assert get_center.status == True
#     assert get_center.center == 'client 1'
    
#     updated_center = models.ClientCenter.update_center(get_session, 1, update_data)
#     get_session.commit()
#     get_session.refresh(updated_center)
    
#     # get the client center after uppdating.
#     get_center = models.ClientCenter.get_center_by_id(get_session, 1)
#     assert get_center.status == False
#     assert get_center.center == 'center 7'