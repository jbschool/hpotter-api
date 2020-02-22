# https://stackoverflow.com/questions/6777524/how-to-automatically-reflect-table-relationships-in-sqlalchemy-or-sqlsoup-orm
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper, relation

engine = create_engine("sqlite://", echo=False)

engine.execute('''
    create table foo (
        id integer not null primary key,
        x integer
    )''')

engine.execute('''
    create table bar (
        id integer not null primary key,
        foo_id integer,
        FOREIGN KEY(foo_id) REFERENCES foo(id)
    )''')

metadata = MetaData()
metadata.reflect(bind=engine)


MAPPERS = {
}

repr_name = lambda t: '%s%s' % (t[0].upper(), t[1:])

for table in metadata.tables:

    cls = None
    # 1. create class object
    cls_name = repr_name(str(table))
    exec("""class %s(object): pass""" % cls_name)
    exec("""cls = %s""" % cls_name)

    # 2. collect relations by FK
    properties = {}
    for c in metadata.tables[table].columns:
        for fk in c.foreign_keys:
            name = str(fk.column).split('.')[0]
            properties.update({
                name: relation(lambda: MAPPERS[repr_name(name)]),
            })

    # 3. map table to class object 
    mapper(cls, metadata.tables[table], properties=properties)
    print('printing --------')
    print(cls)
    print(properties)

    MAPPERS.update({cls_name: cls})

if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker

    print('Mappers: ')
    for m in MAPPERS.values():
        print(m)

    session = sessionmaker(bind=engine)()

    foo = Foo()
    foo.x = 1
    session.add(foo)

    session.commit()

    print(session.query(Foo).all())

    bar = Bar()
    bar.foo = foo
    session.add(bar)
    session.commit()

    print(session.query(Bar).all())