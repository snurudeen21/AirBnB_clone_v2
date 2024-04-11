#!/usr/bin/python3
"""New engine DBStorage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """A class for managing storage with SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        user = environ.get('HBNB_MYSQL_USER')
        password = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST')
        database = environ.get('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects from the current database session"""
        classes = [User, State, City, Amenity, Place, Review]
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
        else:
            for c in classes:
                query = self.__session.query(c).all()
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
