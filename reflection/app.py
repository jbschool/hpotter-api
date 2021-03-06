#!/usr/bin/env python3

from flask import Flask
from schema import schema, db_session
from flask_graphql import GraphQLView

app = Flask(__name__)
app.debug = True

example_query = """
{
  allShellcommands{
    edges{
      node{
        command
        connection{
          createdAt
          sourceIP
          destIP
        }
      }
    }
  }
}
"""

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run()
