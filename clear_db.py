from app.models import *
User.query.delete()
Chat.query.delete()
Message.query.delete()
Link.query.delete()
db.session.commit()

