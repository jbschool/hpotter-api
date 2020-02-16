# HPotter-API

A graphene-sqlalchemy api to request data from the HPotter database

## Getting started

*  `pip3 install -r requirements.txt`
*  `python3 -m app`
*  Navigate to localhost:5000/graphql

Sample query
```
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
```

## Config
In config.yaml
* dbUlr - set the URL for the SQLAlchemy engine
* seedDb - make tables and seed with data. If set to False you must create the DB schema yourself.

## Notes and Credit

This project was initially based on the [graphene-sqlalchemy 2.2.2 release example flask_sqlalchemy project](https://github.com/graphql-python/graphene-sqlalchemy/tree/2.2.2/examples/flask_sqlalchemy)

As of this writing graphene-sqlalchemy==2.2.2 is the latest available on PyPI and will not work with the [2.3.0.dev1 example flask_sqlalchemy project](https://github.com/graphql-python/graphene-sqlalchemy/tree/2.3.0.dev1/examples/flask_sqlalchemy)

