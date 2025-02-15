from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session

import models
from database import engine, session_local


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    id: int
    balance: int

class ServeceBase(BaseModel):
    name: str
    price: int
    
class ReserveMoveyBase(BaseModel):
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

@app.post('/services')
async def create_services(service:ServeceBase, db:db_dependency):
    service = models.Serveces(name=service.name, price=service.price)
    if not service:
        raise HTTPException(404, 'Unknow problem')
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
    
    
@app.post('/reserve')
async def reserve_money(reserve:ReserveMoveyBase, db:db_dependency):
    user = db.query(models.Users).filter(models.Users.id==reserve.from_user_id).first()
    servese = db.query(models.Serveces).filter(models.Serveces.id==reserve.for_service_id).first()
    
    if user and servese:
        if user.balance < servese.price:
            raise HTTPException(404, 'Недостаточно средств!')
        user.balance -= servese.price    
        result = models.ReserveMoney(from_user_id=user.id, for_service_id=servese.id, price=servese.price)
        for i in (result,user): db.add(i)
        db.commit()
        for i in (result,user): db.refresh(i)
        return result
    
    raise HTTPException(404,'Такой услуги или пользователя нет!')


@app.get('/statistic/{id}')
async def get_statistic(id:int, db:db_dependency):
    result = db.query(models.ReserveMoney).filter(models.ReserveMoney.for_service_id==id).all()
    if not result:
        raise HTTPException(404, "Такого id не существует!")
    sum = 0
    for i in result: sum+= i.price
    return {'sum': sum}
    
    
@app.post('/reserve')
async def create_reserve(info:ReserveMoveyBase, db:db_dependency):
    pass

    
