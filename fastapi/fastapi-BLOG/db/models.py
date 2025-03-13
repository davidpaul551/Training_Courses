from db.database_creation import Base
from sqlalchemy import Column,Integer,String,DateTime




class db_PostTable(Base):
    __tablename__ = "Post"
    id = Column(Integer,primary_key=True,index = True)
    image_url=Column(String)
    title = Column(String)
    content = Column(String)
    creator = Column(String)
    timestamp = Column(DateTime)
    