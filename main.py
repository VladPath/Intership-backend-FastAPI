from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session

import models
from database import engine, session_local


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class Users(BaseModel):
    balance: int

class Serveces(BaseModel):
    name: str
    price: int
    
class reserve_movey(BaseModel):
    from_user_id: int
    for_service_id: int
    
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
    

@app.post('/add_money/')
async def add_money(id:int, value:int, db:db_dependency):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    if value <= 0:
        raise HTTPException(404, 'Пополнение не может быть отрицательным')
    if not user:
        user = models.Users(id = id, balance=value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    user.balance += value
    db.commit()
    db.refresh(user)
    return user


    
