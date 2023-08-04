from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class MUser:
    def __init__(self, session):
        self.session = session
    def create(self,name, email):
        # Insert data
        new_user = User(name, email)
        self.session.add(new_user)
        self.session.commit()
    def get(self, pk):
        # Query data
        user = self.session.query(User).filter_by(id=pk).first()
        return user
    def update(self, user, name):
        # Update data
        user.name = 'John Smith'
        self.session.commit()
    def delete(self, user):
        # Delete data
        self.session.delete(user)
        self.session.commit()
