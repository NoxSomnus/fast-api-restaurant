from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from infrastructure.config import engine, Base

from application import router

app = FastAPI()



# Create or update tables defined in the models
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.get('/')
async def index():
    return {'message': 'Hello World'}

app.include_router(router.router)