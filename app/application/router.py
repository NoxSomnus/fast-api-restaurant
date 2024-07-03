from fastapi import APIRouter, HTTPException, Path, Depends
from infrastructure.config import SessionLocal
from sqlalchemy.orm import Session
from domain.aggregates import *
from domain.schemas import *
import application.handlers
from application.response import Response
from application.requests import *

router = APIRouter()

handlers = application.handlers

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#----------------------------------------------INGREDIENTES--------------------------------------------------
@router.post('/ingredients')
async def create_ingredient(request: IngredientSchema, db: Session = Depends(get_db)):
    handlers.create_ingredient(request, db)
    return Response(code="200", status="success", message="Ingredient created successfully", result=None).dict(exclude_none=True)

@router.get('/ingredients/{id}', response_model=Response)
async def get_ingredient_by_id(id: int, db: Session = Depends(get_db)):
    ingredient = handlers.get_ingredient_by_id(id, db)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found") 
    return Response(code="200", status="success", message="Sucess get data", result={ingredient.id,ingredient.name}).dict(exclude_none=True)


@router.get('/ingredients')
async def get_all_ingredients(db: Session = Depends(get_db)):
    ingredients = handlers.get_all_ingredients(db)
    return Response(code="200", status="success", message="Sucess get data", result=ingredients).dict(exclude_none=True)


@router.put('/ingredients/{id}')
async def update_ingredient(id: int, request: str, db: Session = Depends(get_db)):
    handlers.update_ingredient(id, request, db)
    return Response(code="200", status="success", message="Ingredient updated successfully", result=None).dict(exclude_none=True)

@router.delete('/ingredients/{id}')
async def delete_ingredient(id: int, db: Session = Depends(get_db)):
    handlers.delete_ingredient(id, db)
    return Response(code="200", status="success", message="Ingredient deleted successfully", result=None).dict(exclude_none=True)

#----------------------------------------------PLATOS--------------------------------------------------
@router.get('/dishes/{id}', response_model=Response)
async def get_dish_by_id(id: int, db: Session = Depends(get_db)):
    dish = handlers.get_dish_by_id(id, db)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    ingredients_list = []
    dish_ingredients = db.query(Dish_Ingredient).filter(Dish_Ingredient.dish_id == dish.id).all()
    
    for dish_ingredient in dish_ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.id == dish_ingredient.ingredient_id).first()
        ingredient_data = {
            "name": ingredient.name,
            "amount": dish_ingredient.quantity
        }
        ingredients_list.append(ingredient_data)

    result = {
        "id": dish.id,
        "name": dish.name,
        "description": dish.description,
        "instructions": dish.instructions,
        "ingredients": ingredients_list,
        "menu_id": dish.menu_id
    }
    return Response(code="200", status="success", message="Sucess get data", result=result).dict(exclude_none=True)


@router.get('/dishes')
async def get_all_dishes(db: Session = Depends(get_db)):
    dishes = handlers.get_all_dishes(db)
    return Response(code="200", status="success", message="Sucess get data", result=dishes).dict(exclude_none=True)

@router.post('/dishes')
async def create_dish(request: CreateDish, db: Session = Depends(get_db)):
    handlers.create_dish(request, db)
    return Response(code="200", status="success", message="Dish created successfully", result=None).dict(exclude_none=True)

@router.put('/dishes/{id}')
async def update_dish(id: int, request: CreateDish, db: Session = Depends(get_db)):
    handlers.update_dish(id, request, db)
    return Response(code="200", status="success", message="Dish updated successfully", result=None).dict(exclude_none=True)

@router.delete('/dishes/{id}')
async def delete_dish(id: int, db: Session = Depends(get_db)):
    handlers.delete_dish(id, db)
    return Response(code="200", status="success", message="Dish deleted successfully", result=None).dict(exclude_none=True)


#--------------------------------MENU---------------------------------

@router.post('/menus')
async def create_menu(request: MenuSchema, db: Session = Depends(get_db)):
    handlers.create_menu(request, db)
    return Response(code="200", status="success", message="Menu created successfully", result=None).dict(exclude_none=True)

@router.get('/menus/{id}')
async def get_menu_by_id(id: int, db: Session = Depends(get_db)):
    menu = handlers.get_menu_by_id(id, db)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return Response(code="200", status="success", message="Sucess get data", result={menu.id,menu.name}).dict(exclude_none=True)


@router.get('/menus')
async def get_all_menus(db: Session = Depends(get_db)):
    menus = handlers.get_all_menus(db)
    return Response(code="200", status="success", message="Sucess get data", result=menus).dict(exclude_none=True)

@router.delete('/menus/{id}')
async def delete_menu(id: int, db: Session = Depends(get_db)):
    handlers.delete_menu(id, db)
    return Response(code="200", status="success", message="Menu deleted successfully", result=None).dict(exclude_none=True)

@router.put('/menus/{id}')  
async def update_menu(id: int, request: MenuSchema, db: Session = Depends(get_db)):
    handlers.update_menu(id, request, db)
    return Response(code="200", status="success", message="Menu updated successfully", result=None).dict(exclude_none=True)

#--------------------------------Inventario---------------------------------

@router.post('/inventories')
async def create_inventory(request: InventorySchema, db: Session = Depends(get_db)):
    handlers.create_inventory(request, db)
    return Response(code="200", status="success", message="Inventory created successfully", result=None).dict(exclude_none=True)

@router.get('/inventories/{id}')
async def get_inventory_by_id(id: int, db: Session = Depends(get_db)):
    inventory = handlers.get_inventory_by_id(id, db)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return Response(code="200", status="success", message="Sucess get data", result={"ingredient quantity",inventory.quantity}).dict(exclude_none=True)


@router.get('/inventories')
async def get_all_inventories(db: Session = Depends(get_db)):
    inventories = handlers.get_all_inventories(db)
    return Response(code="200", status="success", message="Sucess get data", result=inventories).dict(exclude_none=True)

@router.put('/inventories/{id}')  
async def update_inventory(id: int, request: InventorySchema, db: Session = Depends(get_db)):
    handlers.update_inventory(id, request, db)
    return Response(code="200", status="success", message="Inventory updated successfully", result=None).dict(exclude_none=True)

@router.delete('/inventories/{id}')
async def delete_inventory(id: int, db: Session = Depends(get_db)):
    handlers.delete_inventory(id, db)
    return Response(code="200", status="success", message="Inventory deleted successfully", result=None).dict(exclude_none=True)


#--------------------------------USERS---------------------------------

@router.post('/users')
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    handlers.create_user(request, db)
    return Response(code="200", status="success", message="User created successfully", result=None).dict(exclude_none=True)

@router.get('/users/{id}')
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = handlers.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(code="200", status="success", message="Sucess get data", result=user).dict(exclude_none=True)


@router.get('/users')
async def get_all_users(db: Session = Depends(get_db)):
    users = handlers.get_all_users(db)
    return Response(code="200", status="success", message="Sucess get data", result=users).dict(exclude_none=True)

@router.put('/users/{id}')  
async def update_user(id: int, request: UserSchema, db: Session = Depends(get_db)):
    handlers.update_user(id, request, db)
    return Response(code="200", status="success", message="User updated successfully", result=None).dict(exclude_none=True)

@router.delete('/users/{id}')
async def delete_user(id: int, db: Session = Depends(get_db)):
    handlers.delete_user(id, db)
    return Response(code="200", status="success", message="User deleted successfully", result=None).dict(exclude_none=True)


#--------------------------------ORDERS---------------------------------

@router.post('/orders')
async def create_order(request: OrderSchema, db: Session = Depends(get_db)):
    handlers.create_order(request, db)
    return Response(code="200", status="success", message="Order created successfully", result=None).dict(exclude_none=True)

@router.get('/orders/{id}')
async def get_order_by_id(id: int, db: Session = Depends(get_db)):
    order = handlers.get_order_by_id(id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Response(code="200", status="success", message="Sucess get data", result=order).dict(exclude_none=True)

@router.get('/orders/user/{user_id}')
async def get_orders_by_user_id(user_id: int, db: Session = Depends(get_db)):
    orders = handlers.get_orders_by_user_id(user_id, db)
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return Response(code="200", status="success", message="Sucess get data", result=orders).dict(exclude_none=True)

@router.put('/orders/{id}')  
async def update_order(id: int, status: str, db: Session = Depends(get_db)):
    handlers.update_order(id, status, db)
    return Response(code="200", status="success", message="Order updated successfully", result=None).dict(exclude_none=True)





