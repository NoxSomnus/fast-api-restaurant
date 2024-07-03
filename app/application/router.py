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

@router.put('/inventories/{id}')  
async def update_inventory(id: int, request: InventorySchema, db: Session = Depends(get_db)):
    handlers.update_inventory(id, request, db)
    return Response(code="200", status="success", message="Inventory updated successfully", result=None).dict(exclude_none=True)

@router.delete('/inventories/{id}')
async def delete_inventory(id: int, db: Session = Depends(get_db)):
    handlers.delete_inventory(id, db)
    return Response(code="200", status="success", message="Inventory deleted successfully", result=None).dict(exclude_none=True)



