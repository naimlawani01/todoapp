# Import du framework
import json
from fastapi import FastAPI
import routers.router_todo
import routers.router_auth


app = FastAPI()

# Router dédié aux Tasks
app.include_router(routers.router_todo.router, prefix="/api")

app.include_router(routers.router_auth.router, prefix="/api")
