from tables import Connections as ConnectionsModel
from tables import ShellCommands as ShellCommandsModel
from tables import Credentials as CredentialsModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

class Connections(SQLAlchemyObjectType):
    class Meta:
        model = ConnectionsModel
        interfaces = (relay.Node, )

class ShellCommands(SQLAlchemyObjectType):
    class Meta:
        model = ShellCommandsModel
        interfaces = (relay.Node, )

class Credentials(SQLAlchemyObjectType):
    class Meta:
        model = CredentialsModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    connections = graphene.List(Connections)

    def resolve_connections(self, info):
        query = Connections.get_query(info)
        return query.all()

    credentials = graphene.List(Credentials)

    def resolve_credentials(self, info):
        query = Credentials.get_query(info)
        return query.all()

    # Allow only single column sorting
    all_connections = SQLAlchemyConnectionField(
        Connections, sort=Connections.sort_argument())

    # Allows sorting over multiple columns, by default over the primary key
    all_shellcommands = SQLAlchemyConnectionField(ShellCommands)

    # Disable sorting over this field
    all_credentials = SQLAlchemyConnectionField(Credentials, sort=None)

schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
