from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)

class Services(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class reserve_movey(Base):
    __tablename__ = 'reserve_money'
    
    id = Column(Integer)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    for_service_id = Column(Integer, ForeignKey('services.id'))
    price = Column(Integer, ForeignKey('services.price')) #Не уверен насчет коннекта к price
    













