from sqlalchemy import Boolean, Column, Integer, String
from db.database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class db_users_table(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email = Column(String)
    password = Column(String)
    articleRel = relationship("db_article_table",back_populates="userRel",lazy="joined")


class db_article_table(Base):
    __tablename__ = "articles"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(String)
    published = Column(Boolean)
    user_id=Column(Integer,ForeignKey('users.id'))
    userRel = relationship("db_users_table",back_populates="articleRel")