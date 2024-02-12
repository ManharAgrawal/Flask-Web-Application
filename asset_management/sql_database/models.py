import os
from dotenv import load_dotenv
from sqlalchemy.sql import select
from sqlalchemy.sql import insert
from sqlalchemy.sql import delete
from sqlalchemy.orm import Mapped
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import declarative_base # declarative_base - It allows you to define your database tables as Python classes, making the code more readable and intuitive.
from sqlalchemy import Column, Integer, String
from uuid import uuid4  


#hoisting
load_dotenv() 
user_name = os.getenv('user')
host_name = os.getenv('host')
host_pwd = os.getenv('password')
host_port = os.getenv('port')
user_data = os.getenv('db')

def get_engine(user, password, host, port, db):
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url, pool_size=50, echo=False)
    return engine

engine = get_engine(user_name,host_name,host_port,host_pwd,user_data)
Session = sessionmaker(bind=engine)

# contains a MetaData object where newly defined Table objects are collected. 
# Individual mapped classes are then created by making subclasses of Base.
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(String(), primary_key=True, default=str(uuid4())) 
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    contact = Column(Integer(), nullable=False)
    salary = Column(Integer(), nullable=False)
    department = Column(String(), nullable=False)
    def __repr__(self):  #, the __repr__ method is used to create a string that represents a User instance.
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>" #, contact={self.contact}, salary={self.salary}, department='{self.department}'

session = Session()
    # The mapped_column() directive accepts a superset of arguments that are accepted by the SQLAlchemy Column class.
class UserOps():
    __tablename__ ='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    email:  Mapped[str] = mapped_column(String(40))
    contact: Mapped[int] = mapped_column(Integer)
    salary: Mapped[int] = mapped_column(Integer)
    department: Mapped[str] = mapped_column(String(40))
    
    def insert_user(name, email, contact, salary, department):
        new_user = insert(name=name, email=email, contact=contact, salary=salary, department=department)
        session.add(new_user)
        session.commit() 
        
    def select_user(user_id):
        user_select = select(User)
        result = session.execute(user_select)
        for row in result:
            print(row)
    
    def update_user(user_id, new_values):
        session = Session()
        user = session.query(User).get(user_id)
        if user:
            for key, value in new_values.items():
                setattr(user, key, value)
            session.commit()
            print(f"User with id {user_id} updated successfully.")
        else:
            print(f"User with id {user_id} not found.")
    
    def delete_user(user_id):
        user_delete = delete(User).where(User.id == user_id)
        session.execute(user_delete)
        session.commit()
        
    def delete_table():
        try:
            session.query(User).delete()
            session.commit()
            print("Table deleted successfully.")
        except Exception as e:
            print(f"Error deleting table: {e}")
            session.rollback()
        finally:
            session.close()