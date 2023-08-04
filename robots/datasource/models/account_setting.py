from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AccountSetting(Base):
    __tablename__ = 'account_setting'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    library_id = Column(String)
    card_number = Column(String)
    pin = Column(String)


    def __repr__(self):
        return f"<User(email='{self.name}', password='{self.passwordl}', library_id='{self.library_id}', card_number='{self.card_number}', pin='{self.pin}')>"