from email.policy import default
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable =False)
  city = db.Column(db.String(120), nullable =False)
  state = db.Column(db.String(120), nullable =False)
  address = db.Column(db.String(120), nullable =False)
  phone = db.Column(db.String(120), nullable =False)
  image_link = db.Column(db.String(500), nullable =False)
  facebook_link = db.Column(db.String(120), nullable =False)

#db.create_all()
  
  #Additional Fields
  genres = db.Column(db.String(500), nullable=False)
  website_link = db.Column(db.String(120), nullable =False)
  seeking_description = db.Column(db.String(500), nullable =True, default="")
  seeking_talent = db.Column(db.Boolean, nullable = False )
  venue_show = db.relationship('Show', backref='venue', lazy=True)

def __repr__(self):
    return f'<Venue {self.id} {self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable =False)
  city = db.Column(db.String(120), nullable =False)
  state = db.Column(db.String(120), nullable =False)
  phone = db.Column(db.String(120), nullable =False)
  genres = db.Column(db.String(120), nullable =False)
  image_link = db.Column(db.String(500), nullable =False)
  facebook_link = db.Column(db.String(120), nullable =False)
#db.create_all()
  
  #Additional Fields
  website_link = db.Column(db.String(120))
  seeking_description = db.Column(db.String(500))
  seeking_venue = db.Column(db.Boolean, nullable = False)
  artist_show = db.relationship('Show', backref='artist', lazy=True)

def __repr__(self):
    return f'<Artist {self.id} {self.name}>'
  # TODO: implement any missing fields, as a database migration using Flask-Migrate 

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time= db.Column(db.DateTime)

def __repr__(self):
    return f'<Show {self.id}>'
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

