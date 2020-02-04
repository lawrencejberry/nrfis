from fastapi import FastAPI

from .routers import fbg

app = FastAPI(
    title="NRFIS API",
    description="An API to access sensor data the University of Cambridge's Civil Engineering building",
    version=0.1,
)

app.include_router(fbg.router, prefix="/fbg", tags=["FBG"])

print("HELLO THERE!")
