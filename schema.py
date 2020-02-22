# from models import Connections as ConnectionsModel
# from models import ShellCommands as ShellCommandsModel
# from models import Credentials as CredentialsModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

import sqlalchemy
from database import engine, Base # init_db, 
# init_db()
meta = sqlalchemy.MetaData()
meta.reflect(bind=engine)

MAPPERS = {}
repr_name = lambda t: '%s%s' % (t[0].upper(), t[1:])
for table in meta.tables:
    cls = None
    # 1. create class object
    tabObj =cmdTable = connTable = sqlalchemy.Table(table, meta, autoload=True, autoload_with=engine)
    cls_name = repr_name(str(table))
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
    currMapper = sqlalchemy.orm.class_mapper(cls)
    currMapper.add_properties(properties)
    # sqlalchemy.orm.mapper(cls, meta.tables[table], properties=properties)
    # print('printing --------')
    # print(cls)
    # print(properties)

    MAPPERS.update({cls_name: cls})

# print('Print mappers: ------')
# print(MAPPERS)

def make_gql_class(new_class_name, table_name):
    namespace = dict(
        Meta = type('Meta', (object, ), dict(
            model = MAPPERS[table_name],
            interfaces = (relay.Node, )
            )
        )
    )

    newClass = type(new_class_name, (SQLAlchemyObjectType, ), namespace)
    return newClass


for tableName in MAPPERS:
    className = tableName + 'Gql'
    exec('%s = make_gql_class("%s", "%s")' % (className, className, tableName))

# ConnectionsGql = make_gql_class('ConnectionsGql', 'Connections')
# ShellCommandsGql = make_gql_class('ShellcommandsGql', 'Shellcommands')
# CredentialsGql = make_gql_class('CredentialsGql', 'Shellcommands')

# class ConnectionsGql(SQLAlchemyObjectType):
#     class Meta:
#         model = MAPPERS['Connections'] # Connections
#         interfaces = (relay.Node, )

# class ShellCommandsGql(SQLAlchemyObjectType):
#     class Meta:
#         model = Shellcommands
#         interfaces = (relay.Node, )

# class CredentialsGql(SQLAlchemyObjectType):
#     class Meta:
#         model = Credentials
#         interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # Allow only single column sorting
    all_connections = SQLAlchemyConnectionField(
        ConnectionsGql, sort=ConnectionsGql.sort_argument())

    # Allows sorting over multiple columns, by default over the primary key
    all_shellcommands = SQLAlchemyConnectionField(ShellcommandsGql)

    # Disable sorting over this field
    all_credentials = SQLAlchemyConnectionField(CredentialsGql, sort=None)

schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
