    from models import Connections as ConnectionsModel
    from models import ShellCommands as ShellCommandsModel
    from models import Credentials as CredentialsModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

import sqlalchemy
from database import engine, init_db, Base
# init_db()
meta = sqlalchemy.MetaData()
meta.reflect(bind=engine)

connTable = meta.tables['connections']
connTable = sqlalchemy.Table('connections', meta, autoload=True, autoload_with=engine)

repr_name = lambda t: '%s%s' % (t[0].upper(), t[1:])

cmdTable = connTable = sqlalchemy.Table('shellcommands', meta, autoload=True, autoload_with=engine)

MAPPERS = {}
repr_name = lambda t: '%s%s' % (t[0].upper(), t[1:])
for table in meta.tables:
    cls = None
    # 1. create class object
    tabObj =cmdTable = connTable = sqlalchemy.Table(table, meta, autoload=True, autoload_with=engine)
    cls_name = repr_name(str(table))
    # exec("""class %s(object): pass""" % cls_name)
    classDef = """class %s(Base):
        __table__ = tabObj
    """
    exec(classDef % cls_name)
    exec("""cls = %s""" % cls_name)

    # 2. collect relations by FK
    properties = {}
    for c in meta.tables[table].columns:
        for fk in c.foreign_keys:
            name = str(fk.column).split('.')[0]
            properties.update({
                name: sqlalchemy.orm.relation(lambda: MAPPERS[repr_name(name)]),
            })

    # 3. map table to class object 
    sqlalchemy.orm.mapper(cls, meta.tables[table], properties=properties)
    print('printing --------')
    print(cls)
    print(properties)

    MAPPERS.update({cls_name: cls})

print(MAPPERS)

# table = meta.tables['shellcommands']
# cls_name = repr_name(str(table))
# exec("""class %s(object): pass""" % cls_name)
# exec("""cls = %s""" % cls_name)
# print(cls)

# name = 'connections'
# MAPPERS = {
# }
# properties = {}
# properties.update({
#     name: sqlalchemy.orm.relationship(lambda: MAPPERS[repr_name(name)]),
#     })
# print(properties)

# sqlalchemy.orm.mapper(cls, meta.tables[table], properties=properties)

# cls = repr_name(str(meta.tables['shellcommands']))
# temp = repr_name('Connections')
# properties = {'connections', sqlalchemy.orm.relationship(temp)}
# print('printing ------')
# print(cls)
# print(properties)
# sqlalchemy.orm.mapper(cls, cmdTable, properties)

# for col in cmdTable.columns:
#     print(col)

class ModelMaker(Base):
    __table__ = connTable

class CmdMaker(Base):
    __table__ = cmdTable
    # connection = sqlalchemy.orm.relationship('Connections')

class Connections(SQLAlchemyObjectType):
    class Meta:
        model = ModelMaker
        interfaces = (relay.Node, )

class ShellCommands(SQLAlchemyObjectType):
    class Meta:
        model = CmdMaker
        interfaces = (relay.Node, )

class Credentials(SQLAlchemyObjectType):
    class Meta:
        model = CredentialsModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # Allow only single column sorting
    all_connections = SQLAlchemyConnectionField(
        Connections, sort=Connections.sort_argument())

    # Allows sorting over multiple columns, by default over the primary key
    all_shellcommands = SQLAlchemyConnectionField(ShellCommands)

    # Disable sorting over this field
    all_credentials = SQLAlchemyConnectionField(Credentials, sort=None)

schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
