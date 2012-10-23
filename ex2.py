from sqlalchemy import*

db = create_engine('sqlite:///tutorial2.db')
# The create_engine() function takes a single parameter that's a URI, of the form:
# "engine://user:password@host:port/database"
# Most of these options can be omitted,
db.echo = False

metadata = MetaData(bind=db)
#Before creating our table definitions we have to create the object that will manage them.
users2 = Table('users2', metadata,
    Column('user_id', Integer, primary_key = True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String),
    )
#users2.create()
ins = users2.insert()
ins.execute(name = "Tony", age = 21, password = "monkmonk12")
ins.execute({'name': "Tom", 'age': 33, 'password': "hungryhippo"},
    {'name': "Tina", 'age': 13, 'password': "turtleteeth"},
    {'name': "Ralf", 'age': 23, 'password': "riffraff"},
    {'name': "Zack", 'age': 14, 'password': "executables"},
    )

sel = users2.select()
rs = sel.execute()

row = rs.fetchone()
print 'ID:', row[0] # can also be row.uder_id
print 'Name:', row.name # can also be row[1]
print 'Age:', row.age # can also be row[2]
print 'password:', row.password

for row in rs:
    print "%r is %r years old!" % (row.name, row.age)