from db.database_creation import Base
from sqlalchemy import Column , Integer , String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class db_User_table(Base):
    __tablename__ = 'User'
    id = Column(Integer , primary_key=True,index=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    items = relationship('db_Post_table',back_populates='user')


class db_Post_table(Base):
    __tablename__ = 'Post'
    id = Column(Integer , primary_key=True,index=True)
    image_url = Column(String)
    image_url_type= Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id= Column(Integer,ForeignKey('User.id'))
    user = relationship('db_User_table',back_populates='items')
    comments = relationship('db_Comments_table',back_populates="post")

class db_Comments_table(Base):
    __tablename__ = "Comments"
    id = Column(Integer,primary_key=True,index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer,ForeignKey('Post.id'))
    post = relationship('db_Post_table',back_populates="comments")