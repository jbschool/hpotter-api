import sqlalchemy
from database import engine, init_db

init_db()

meta = sqlalchemy.MetaData()
meta.reflect(bind=engine)

print(meta.tables['connections'].columns)

print("---tables------")
for key, table in meta.tables.items():
    print(table)
    for col in table.columns:
        print(str(col) + '\t' + str(col.type))


print("end")