import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

import yaml

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

def load_config():
    config = {}
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config

config = load_config()

engine = create_engine(config['dbUrl'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

meta = sqlalchemy.MetaData()
meta.reflect(bind=engine)

MAPPERS = {}
cap_first_char = lambda t: '%s%s' % (t[0].upper(), t[1:])
lower_first_char = lambda t: '%s%s' % (t[0].lower(), t[1:])
for table in meta.tables:
    cls = None
    # 1. create class object
    tabObj = sqlalchemy.Table(table, meta, autoload=True, autoload_with=engine)
    cls_name = cap_first_char(str(table))
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
                name: sqlalchemy.orm.relation(lambda: MAPPERS[cap_first_char(name)]),
            })

    # 3. map table to class object 
    currMapper = sqlalchemy.orm.class_mapper(cls)
    currMapper.add_properties(properties)
    # sqlalchemy.orm.mapper(cls, meta.tables[table], properties=properties)

    MAPPERS.update({cls_name: cls})

GRAPH_QL_SUFFIX = 'Gql'
def make_gql_class(table_class_name):
    namespace = dict(
        Meta = type('Meta', (object, ),
            dict(
                model = MAPPERS[table_class_name],
                interfaces = (relay.Node, ))
        )
    )

    newClass = type(table_class_name + GRAPH_QL_SUFFIX, (SQLAlchemyObjectType, ), namespace)
    return newClass

for table_class_name in MAPPERS:
    className = table_class_name + GRAPH_QL_SUFFIX
    exec('%s = make_gql_class("%s")' % (className, table_class_name))
    # ConnectionsGql = make_gql_class('Connections')

def make_connection_field_assignment(table_class_name):
    table_name = lower_first_char(table_class_name)
    className = table_class_name + GRAPH_QL_SUFFIX
    code = 'all_%s = SQLAlchemyConnectionField(%s)' % (table_name, className)
    # all_connections = SQLAlchemyConnectionField(ConnectionsGql)
    return code

connection_fields = []
for table_class_name in MAPPERS:
    assignment = make_connection_field_assignment(table_class_name)
    connection_fields.append(assignment)

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    for assignment in connection_fields:
        exec(assignment)

schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
