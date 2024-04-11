
import os
import sys

from fastapi import FastAPI

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from .api.routers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)
