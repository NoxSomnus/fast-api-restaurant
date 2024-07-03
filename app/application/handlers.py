from sqlalchemy.orm import Session
from domain.aggregates import *
from domain.schemas import *
from application.requests import *
from fastapi import HTTPException

#-------------------------------------------- PLATOS ---------------------------------------------------
def create_dish(request: CreateDish, db: Session):
    # Crear el plato
    dish = Dish(name=request.name, description=request.description, instructions=request.instructions, menu_id=request.menu_id)
    db.add(dish)
    db.flush()  # Asigna un ID al plato sin hacer commit

    # Procesar los ingredientes
    for ingredient_id, quantity in zip(request.ingredients, request.ingredients_quantities):
        registered_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if registered_ingredient:
            dish_ingredient = Dish_Ingredient(
                dish_id=dish.id,
                ingredient_id=registered_ingredient.id,
                quantity=quantity
            )
            db.add(dish_ingredient)

    # Commit y refresh
    db.commit()
    db.refresh(dish)
    return dish

def get_dish_by_id(id: int, db: Session):
    dish = db.query(Dish).filter(Dish.id == id).first()
    return dish

def get_all_dishes(db: Session):
    dishes = db.query(Dish).all()
    return dishes

def update_dish(id: int, request: CreateDish, db: Session):
    dish = db.query(Dish).filter(Dish.id == id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
        
    dish.name = request.name
    dish.description = request.description
    dish.instructions = request.instructions
    
    # Eliminar los ingredientes existentes para este plato
    db.query(Dish_Ingredient).filter(Dish_Ingredient.dish_id == dish.id).delete()
    
    # Procesar los ingredientes actualizados
    for ingredient_id, quantity in zip(request.ingredients, request.ingredients_quantities):
        registered_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if registered_ingredient:
            dish_ingredient = Dish_Ingredient(
                dish_id=dish.id,
                ingredient_id=registered_ingredient.id,
                quantity=quantity
            )
            db.add(dish_ingredient)

    db.commit()
    db.refresh(dish)
    return dish

def delete_dish(id: int, db: Session):
    dish = db.query(Dish).filter(Dish.id == id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()
    return None

#---------------------------- INGREDIENTS -------------------------------------------------------------
def create_ingredient(request: IngredientSchema, db: Session):
    ingredient = Ingredient(id=request.id,name=request.name)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def get_ingredient_by_id(id: int, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    return ingredient

def get_all_ingredients(db: Session):
    ingredients = db.query(Ingredient).all()
    return ingredients

def update_ingredient(id: int, request: str, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient.name = request
    db.commit()
    db.refresh(ingredient)
    return ingredient

def delete_ingredient(id: int, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(ingredient)
    db.commit()
    return None

#----------------------------------------------Menus--------------------------------------------------
def create_menu(request: MenuSchema, db: Session):
    menu = Menu(name=request.name, description=request.description)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu

def get_menu_by_id(id: int, db: Session):
    menu = db.query(Menu).filter(Menu.id == id).first()
    return menu

def get_all_menus(db: Session):
    menus = db.query(Menu).all()
    return menus

def update_menu(id: int, request: MenuSchema, db: Session):
    menu = db.query(Menu).filter(Menu.id == id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu.name = request.name
    menu.description = request.description
    db.commit()
    db.refresh(menu)
    return menu

def delete_menu(id: int, db: Session):
    menu = db.query(Menu).filter(Menu.id == id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    db.delete(menu)
    db.commit()
    return None

#----------------------------------------------Inventario-----------------------------------------------

def create_inventory(request: InventorySchema, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.id == request.ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    inventory = Inventory(ingredient_id=request.ingredient_id, quantity=request.quantity)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def get_inventory_by_id(id: int, db: Session):
    inventory = db.query(Inventory).filter(Inventory.ingredient_id == id).first()
    return inventory

def get_all_inventories(db: Session):
    inventory = db.query(Inventory).all()
    return inventory

def update_inventory(id: int, request: InventorySchema, db: Session):
    inventory = db.query(Inventory).filter(Inventory.ingredient_id == id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    inventory.quantity = request.quantity
    db.commit()
    db.refresh(inventory)
    return inventory

def delete_inventory(id: int, db: Session):
    inventory = db.query(Inventory).filter(Inventory.ingredient_id == id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    db.delete(inventory)
    db.commit()
    return None

#----------------------------------------------User--------------------------------------------------

def create_user(request: UserSchema, db: Session):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail="Email in use")
    
    user = db.query(User).filter(User.username == request.username).first()
    if user:
        raise HTTPException(status_code=409, detail="Username already exists")

    new_user = User(name=request.name, email=request.email, password=request.password, username=request.username, role=request.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id: int, db: Session):    
    user = db.query(User).filter(User.id == id).first()
    return user

def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def update_user(id: int, request: UserSchema, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = request.name
    user.email = request.email
    user.password = request.password
    user.username = request.username
    user.role = request.role
    db.commit()
    db.refresh(user)
    return user

def delete_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None

#----------------------------------------------Order--------------------------------------------------

def create_order(request: OrderSchema, db: Session):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    dish = db.query(Dish).filter(Dish.id == request.dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    for ingredient in dish.ingredients:
        ingredient_dish = db.query(Dish_Ingredient).filter(Dish_Ingredient.dish_id == dish.id, Dish_Ingredient.ingredient_id == ingredient.id).first()
        if not ingredient_dish:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        inventory = db.query(Inventory).filter(Inventory.ingredient_id == ingredient.id).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")
        if inventory.quantity < ingredient_dish.quantity:
            raise HTTPException(status_code=400, detail="Insufficient ingredient in inventory - {}".format(ingredient.name))
        inventory.quantity -= ingredient_dish.quantity

    order = Order(user_id=user.id, dish_id=dish.id, quantity=request.quantity, status=request.status)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return order

def get_order_by_id(id: int, db: Session):
    order = db.query(Order).filter(Order.id == id).first()
    return order

def update_order(id: int, status: str, db: Session):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_user_id(id: int, db: Session):
    orders = db.query(Order).filter(Order.user_id == id).all()
    return orders
