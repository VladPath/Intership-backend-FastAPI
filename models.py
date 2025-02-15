from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Da
from database import Base


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)

class Serveces(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class ReserveMoney(Base):
    __tablename__ = 'reserve_moneys'
    
    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    for_service_id = Column(Integer, ForeignKey('services.id'))
    price = Column(Integer, default=0)
    at_created = Column()



    













