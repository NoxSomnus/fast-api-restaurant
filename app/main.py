from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from infrastructure import auth
from infrastructure.config import engine, Base
from application.routers import ingredient_router, dish_router, menu_router, inventary_router, order_router, user_router

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create or update tables defined in the models
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.get('/')
async def index():
    return {'message': 'Hello World'}

app.include_router(auth.router)
app.include_router(ingredient_router.router)
app.include_router(dish_router.router)
app.include_router(menu_router.router)
app.include_router(inventary_router.router)
app.include_router(order_router.router)
app.include_router(user_router.router)