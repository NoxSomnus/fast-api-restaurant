from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from infrastructure import auth
from infrastructure.config import engine, Base
from application.routers import dish_router, menu_router, order_router, user_router, ingredient_router, inventary_router

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create or update tables defined in the models
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.get('/')
async def index():
    return {'message': 'Hello World'}

app.include_router(auth.router)
app.include_router(dish_router.router)
app.include_router(menu_router.router)
app.include_router(order_router.router)
app.include_router(user_router.router)
app.include_router(ingredient_router.router)
app.include_router(inventary_router.router)
