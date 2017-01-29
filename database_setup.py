from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from text_type import CoerceUTF8

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    picture = Column(String(250))

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'id': self.id,
            'picture': self.picture
        }


class Category(Base):
    __tablename__ = 'category'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Book(Base):
    __tablename__ = 'book'

    title = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    author = Column(CoerceUTF8(250))
    img = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    user = relationship(User)
    category = relationship(Category)

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        return {
            'name': self.title,
            'id': self.id,
            'author': self.author,
            'img': self.img,
        }

engine = create_engine('sqlite:///books.db')
Base.metadata.create_all(engine)
