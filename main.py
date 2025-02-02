# main code.
# The main point of call.
from fastapi import FastAPI
from schema import *
from db.session import engine, Session
from db import client_model as models
from apis.client import client_router
from apis.user_group import user_group_router
from apis.client_user import user_router
from apis.client_center import center_router
from apis.user_center import user_center_router
from apis.equipment import equipment_router
from apis.permissions import permission_router
from apis.user_group_permission import user_permit_router
from apis.departments_type_api import user_departments_type_router
from apis.gender_api import gender_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio
import os
from tests.seeder import (
    seed_client_prod,
    seed_client_user_prod
)

# Microservice description
description = "Acess Control Application"
tags_metadata =[
    {
        "name":"Client",
        "description":"Client Notification Crud",
    }
]

access_control_app = FastAPI(
    title="Access Control API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# create the tables.
models.Base.metadata.create_all(engine)

# allowed host.
origins =[]
access_control_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

async def main() -> None:
    config = uvicorn.Config(
        "main:access_control_app", 
        host=os.getenv("HOST"), 
        port=int(os.getenv("ACCESS_PORT")), 
        reload=os.getenv("RELOAD"),
        workers=1, 
        loop="asyncio")
    
    server = uvicorn.Server(config)
    await server.serve()

# include client router.
access_control_app.include_router(
    client_router
)
# include the user router.
access_control_app.include_router(
    user_router
)
# include the center router.
access_control_app.include_router(
    center_router
)
# include the user_group router
access_control_app.include_router(
    user_group_router
)
# include the user center router.
access_control_app.include_router(
    user_center_router
)
# include the equipment router.
access_control_app.include_router(
    equipment_router
)
# include the permission router.
access_control_app.include_router(
    permission_router    
)
# include the user group permission router
access_control_app.include_router(
    user_permit_router
)
# include the gender api router
access_control_app.include_router(
    gender_router
)
# include the department type api
access_control_app.include_router(
    user_departments_type_router
)

@access_control_app.on_event("startup")
async def startup_event():
    db = Session()
    if not os.environ['TESTING']:
        seed_client_prod(db)
        seed_client_user_prod(db)
    db.close()
    
    
@access_control_app.get("/")
async def ping():
    return {"detail": "Access Control Application is up"}

if __name__ == "__main__":
    # Run the FastAPI app
    asyncio.run(main())