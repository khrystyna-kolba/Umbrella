from main import db
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    cityname = db.Column(db.String(100), nullable=False)
    #title = db.Column(db.String(100), nullable=False)
    #author = db.Column(db.String(100), nullable=False)
    #date = db.Column(db.Date, nullable=False)
    #status = db.Column(db.String(100), nullable=False)
    #def __repr__(self):
      #  return f'{self.title}, author {self.author} created on {self.date} status: {self.status}'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)