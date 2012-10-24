# Joins

from sqlalchemy import *

db = create_engine('sqlite:///joinDbDemo.db')
db.echo = True
metadata = MetaData(bind=db)

users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
)
#users.create()

emails = Table('emails', metadata,
    Column('email_id', Integer, primary_key=True),
    Column('address', String),
    Column('user_id', Integer, ForeignKey('users.user_id')),
)
#emails.create()

i = users.insert()
i.execute(
    {'name': 'Mary', 'age': 30},
    {'name': 'John', 'age': 42},
    {'name': 'Susan', 'age': 57},
    {'name': 'Carl', 'age': 33}
)

i = emails.insert()
i.execute(
    # There's a better way to do this, but we haven't gotten there yet
    {'address': 'mary@example.com', 'user_id': 1},
    {'address': 'john@nowhere.net', 'user_id': 2},
    {'address': 'john@example.org', 'user_id': 2},
    {'address': 'susan@example.com', 'user_id': 3},
    {'address': 'carl@nospam.net', 'user_id': 4},
)

def run(stmt):
    rs =stmt.execute()
    for row in rs:
        print row

s = select([users, emails], emails.c.user_id == users.c.user_id)
run(s)
