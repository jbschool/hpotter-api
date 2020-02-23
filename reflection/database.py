import yaml
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

def init_db():

    # import models here so that they will be registered properly
    # on the metadata.  Otherwise need to import them first
    # before calling init_db()
    from tables import Connections, ShellCommands, Credentials
    from ipaddress import ip_address
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    conn1 = Connections(
        sourceIP = ip_address('127.0.0.1'),
        sourcePort = 80,
        destIP = ip_address('127.0.0.1'),
        destPort = 8080,
        proto = 1
    )
    db_session.add(conn1)
    conn2 = Connections(
        sourceIP = ip_address('127.0.0.2'),
        sourcePort = 81,
        destIP = ip_address('127.0.0.2'),
        destPort = 8081,
        proto = 2
    )
    db_session.add(conn2)

    cmd1 = ShellCommands(
        command = 'cd /',
        connection = conn1
    )
    db_session.add(cmd1)

    cmd2 = ShellCommands(
        command = './attach.sh',
        connection = conn2
    )
    db_session.add(cmd2)

    creds1 = Credentials(
        username = 'darth',
        password = 'theRealDarkLord',
        connection = conn1
    )
    db_session.add(creds1)

    creds2 = Credentials(
        username = 'voldemort',
        password = 'johnnyCash',
        connection = conn2
    )
    db_session.add(creds2)

    db_session.commit()

if __name__ == '__main__':
    from database import init_db
    init_db()