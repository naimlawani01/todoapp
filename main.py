# Import du framework
import json
from fastapi import FastAPI
import routers.router_todo
import routers.router_auth
from docs.description import api_description
from docs.tags import tags_metadata


app = FastAPI(title="TODO API",description=api_description,openapi_tags= tags_metadata)

# Router dédié aux Tasks
app.include_router(routers.router_todo.router, prefix="/api")

app.include_router(routers.router_auth.router, prefix="/api")
