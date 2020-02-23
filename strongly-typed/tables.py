from database import Base

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import IPAddressType

import graphene
from graphene_sqlalchemy.converter import convert_sqlalchemy_type

# https://github.com/graphql-python/graphene-sqlalchemy/issues/257
@convert_sqlalchemy_type.register(IPAddressType)
def convert_column_to_string(type, column, registry=None):
    return graphene.String

class Connections(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    sourceIP = Column(IPAddressType)
    sourcePort = Column(Integer)
    destIP = Column(IPAddressType)
    destPort = Column(Integer)
    proto = Column(Integer)

class ShellCommands(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    command = Column(String)
    connections_id = Column(Integer, ForeignKey('connections.id'))
    connection = relationship('Connections')

class Credentials(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    connections_id = Column(Integer, ForeignKey('connections.id'))
    connection = relationship('Connections')
