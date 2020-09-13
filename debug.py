from app.models import *

u = User(username='u', password='1')
v = User(username='v', password='2')
db.session.add(u)
db.session.add(v)
db.session.commit()
c = Chat(users=User.query.all())
db.session.add(c)
db.session.commit()
m = Message(sent_from=u, sent_to=v, message="hello, v", chat=c)
db.session.add(m)
db.session.commit()


