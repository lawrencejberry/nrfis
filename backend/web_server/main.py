from fastapi import FastAPI

from .routers import fbg

app = FastAPI()

app.include_router(fbg.router, prefix="/fbg", tags=["FBG"])
