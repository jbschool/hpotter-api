import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import graphene
from graphene import relay, Schema
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from yaml import safe_load

def load_config():
    config = {}
    with open('config.yaml', 'r') as f:
        config = safe_load(f)
    return config

config = load_config()

engine = create_engine(config['dbUrl'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Execute declaration of classes relflected from database tables
# in the module scope
CLSNAME_TO_CLS_MAP = {}
cap_first_char = lambda t: '%s%s' % (t[0].upper(), t[1:])
lower_first_char = lambda t: '%s%s' % (t[0].lower(), t[1:])
meta = sqlalchemy.MetaData()
meta.reflect(bind=engine)
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
                name: sqlalchemy.orm.relation(
                        lambda: CLSNAME_TO_CLS_MAP[cap_first_char(name)]
                    ),
            })

    # 3. add relation properties to ORM for reflected classes 
    sqlalchemy.orm.class_mapper(cls).add_properties(properties)

    # 4. save a reference to the class object
    CLSNAME_TO_CLS_MAP.update({cls_name: cls})

GRAPH_QL_SUFFIX = 'Gql'

# Construct and return a class inherited from SQLAlchemyObjectType
def make_gql_class(table_class_name):
    namespace = dict(
        Meta = type('Meta', (object, ),
            dict(
                model = CLSNAME_TO_CLS_MAP[table_class_name],
                interfaces = (relay.Node, ))
        )
    )

    newClass = type(table_class_name + GRAPH_QL_SUFFIX, (SQLAlchemyObjectType, ), namespace)
    return newClass

# Construct a connection field assignment statement
def make_connection_field_assignment(table_class_name):
    table_name = lower_first_char(table_class_name)
    className = table_class_name + GRAPH_QL_SUFFIX
    code = 'all_%s = SQLAlchemyConnectionField(%s)' % (table_name, className)
    # all_connections = SQLAlchemyConnectionField(ConnectionsGql)
    return code

# Execute declaration of classes inherited from SQLAlchemyObjectType 
# in the module scope for connection fields
for table_class_name in CLSNAME_TO_CLS_MAP:
    className = table_class_name + GRAPH_QL_SUFFIX
    exec('%s = make_gql_class("%s")' % (className, table_class_name))
    # ConnectionsGql = make_gql_class('Connections')

# Build all connection field assignment statements
connection_fields = []
for table_class_name in CLSNAME_TO_CLS_MAP:
    assignment = make_connection_field_assignment(table_class_name)
    connection_fields.append(assignment)

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # Execute connection field assignment statements in class scope
    for assignment in connection_fields:
        exec(assignment)

schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
