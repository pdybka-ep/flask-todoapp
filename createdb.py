from todoapp import app
from models import db
db.create_all()

from models import Category
work = Category(name=u'work')
home = Category(name=u'home')

db.session.add(work)
db.session.add(home)
db.session.commit()

from models import Priority

high = Priority(name=u'high', value=3)
medium = Priority(name=u'medium', value=2)
low = Priority(name=u'low', value=1)

db.session.add(high)
db.session.add(medium)
db.session.add(low)
db.session.commit()
