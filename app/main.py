from fastapi import FastAPI

from app.transport.vinyl import vinyl_router


app = FastAPI()
app.include_router(vinyl_router)
