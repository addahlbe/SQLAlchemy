#Mapping your objects to SQL rows

from sqlalchemy import *
from sqlalchemy.orm import *
db = create_engine('sqlite:///joinDbDemo.db')
db.echo = True

metadata = MetaData(bind = db)
# because users and emails tables are already in the database, we don't have to specify them again. We can just 
# let SQLAlchemy fetch their definitions from the database.
users = Table('users', metadata, autoload=True)
emails = Table('emails', metadata, autoload=True)

# These are empty classes that will become our data classes
class User(object):
    pass
class Email(object):
    pass

#This is where the magic happens! The mapper() function take a minimum of two parameters:
#First the data class to modify, and then the table object onto which the data class should be mapped.
# The data class will have attributes automatically added to it that correspond to the columns of your database table.
# ex. User.user_id, User.age -> Email.email_id, Email.address
usermapper = mapper(User, users)
emailmapper = mapper(Email, emails)

# SQLA is capable of automatically keeping track of all the data objects you create, and any changes you make to their attributes.
session = create_session()

# now that we have created a session object we can use it to load some data from our database.
mary = session.query(User).selectfirst(users.c.name=='Mary')
# now that we have an instance of the data class we can manipulate its attributes just like a normal object.
mary.age += 1
# SQLA will keep track of the changes we make, but won't actually send them out to the database riht away.
# To send our changes to the database we need to..:
session.flush()

fred = User()
fred.name = 'Fred'
fred.age = 37

print "About to flush() without a save()..."
session.flush() #will not save fred's data yet

session.save(fred)
print "Just called save(). Now flush() will actually do something!"
session.flush() #now fred's data will be saved

# Deletes are like inserts, are done by calling a method on the Session object. Note that his does not delete the fred instance 
# from your own code, it just flags it as deleted in the Session objects internal object tracker. The fred instance will still be around,
# accessible to your own code, until you run a "del fred" statement.
session.delete(fred)
session.flush()