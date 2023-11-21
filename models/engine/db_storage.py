#!/usr/bin/python3
""" db storage class"""
from os import getenv
from models.base_model import Base, Amenity, City, Place, Review, State, User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """storage engine."""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True
                                      )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        if cls is None:
            queries = [State, City, User, Place, Review, Amenity]
            objs = [self.__session.query(query).all() for query in queries]
        else:
            cls = eval(cls) if isinstance(cls, str) else cls
            objs = self.__session.query(cls).all()
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        self.__session.close()
