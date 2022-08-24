from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

#db.create_all()
  
  #Additional Fields
  website_link = db.Column(db.String(120))
  Seeking_Description = db.Column(db.String(500))
  Looking_Venue = db.Column(db.Boolean, nullable = False)
  Venue_Show = db.relationship('Show', backref='venue', lazy=True)

def __repr__(self):
    return f'<Venue {self.id} {self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
#db.create_all()
  
  #Additional Fields
  website_link = db.Column(db.String(120))
  Seeking_Description = db.Column(db.String(500))
  Looking_Artist = db.Column(db.Boolean, nullable = False)
  Artist_Show = db.relationship('Show', backref='artist', lazy=True)

def __repr__(self):
    return f'<Artist {self.id} {self.name}>'
  # TODO: implement any missing fields, as a database migration using Flask-Migrate 

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  Artist_ID = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  Venue_ID = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  Start_Time= db.Column(db.DateTime)

def __repr__(self):
    return f'<Show {self.id}>'
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

