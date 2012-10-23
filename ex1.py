# sqlalchemy tutorial
import sqlalchemy
print sqlalchemy.__version__

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy import select
# object that knows how to communicate with the provided databse using the credentials you supply.
# In this case we are using a sqlite database that doesn't need credentials.
engine = create_engine('sqlite:///tutorial.db', echo = True)
# Notice we set echo to true, this means SqlAlchemy will output all the SQL command it is executing to stdout.
# This is hand for debugging, but should be set to False when you're ready to put the code into production.
metadata = MetaData(bind=engine)

users_table = Table('users', metadata,
    Column('id', Integer, primary_key = True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String),
    )
# Creating tables programatically. Done by using sql's table and column objects.
# We create a database and name it users. The Id column is set to our primary key. 
# Sqlalchemy will magically incriment this for us as we add users to the database.
addresses_table = Table('addresses', metadata,
    Column('id', Integer, primary_key = True),
    Column('user_id', None, ForeignKey('users.id')),
    Column('email_address', String, nullable=False)
    )
# The only major differenct to the address table is how we set up the Foreign key attribute to connect the two tables.
# basically we point the other table by passing the correct field name in a string to the ForeignKey object.
metadata.create_all()

# create an insert object
ins = users_table.insert()

#add values to the insert object
new_user = ins.values(name = "Tony", age = 20, password = "pass")

#create a database connection
conn = engine.connect()
# add a user to database by executing SQL
conn.execute(new_user)

# another way to insert conectionlessly:

ins2 = users_table.insert()
result = engine.execute(ins, name = "Shinji", age = 15, password = "pass")
# another connectionless insert
result2 = users_table.insert().execute(name = "Martha", age = 45, password = "pass")

# how to insert multiple rows
conn.execute(users_table.insert(), [
    {"name": "Ted", "age": 10, "password": "dink"},
    {"name": "Sam", "age": 15, "password": "troy"},
    {"name": "Tony", "age": 21, "password": "monkmonk12"}
    ])

s = select([users_table])
result = s.execute()

for row in result:
    print row

