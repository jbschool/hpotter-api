# HPotter-API

A graphene-sqlalchemy api to request data from the HPotter database

## Getting started

This POC has two examples. 
*  `strongly-typed` shows how graphene-sqlalchemy can be used to expose data using pre-defined table classes
*  `reflection` shows how, given a database, reflection can be used to expose every table

### Reflection
* `cd reflection`
* `pip3 install -r requirements.txt`
* First Time Only
    * A DB is needed to reflect. Create a sample DB with
    * `python3 -m create_db`
*  `python3 -m app`
*  Navigate to `localhost:5000/graphql`
*  Query the DB!!!

### Strongly-Typed
* `cd strongly-typed`
* `pip3 install -r requirements.txt`
*  `python3 -m app`
*  Navigate to `localhost:5000/graphql`
*  Query the DB!!!

## Querying
In this POC, Flask provides an easy way to explore data available and autocomplete for queries. For example, start typing `{ allShell`.

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
* seedDb - for strongly-typed example, automatically make tables and seed with data. If set to False you must create the DB schema yourself.

## Notes and Credit

This project was initially based on the [graphene-sqlalchemy 2.2.2 release example flask_sqlalchemy project](https://github.com/graphql-python/graphene-sqlalchemy/tree/2.2.2/examples/flask_sqlalchemy)

As of this writing graphene-sqlalchemy==2.2.2 is the latest available on PyPI and will not work with the [2.3.0.dev1 example flask_sqlalchemy project](https://github.com/graphql-python/graphene-sqlalchemy/tree/2.3.0.dev1/examples/flask_sqlalchemy)

