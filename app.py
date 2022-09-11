#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from os import abort
import re
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from sqlalchemy import distinct
import logging
from logging import Formatter, FileHandler, exception
from flask_wtf import Form
from flask_wtf import CSRFProtect
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
import sys
#Import Models

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

#with app.app_context():
 # db.create_all()
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  response_data = []

  try:
    city_state = db.session.query(distinct(Venue.city), Venue.state).all()

    date_today = datetime.datetime.now()
    for location in city_state:
      city = location[0]
      state = location[1]

      location_values = {"city" : city, "state" : state, "venues": []}
      venues = Venue.query.filter_by(city=city, state=state).all()

      for v in venues:
        venue_ID = v.id
        venue_name = v.name

        upcoming_shows = (
          db.session.query(Show).join(Venue).filter_by(venue_ID==venue_ID).filter(Show.start_time > date_today).all()
        )

        venue_data ={
          "id" : venue_ID,
          "name" : venue_name,
          "num_upcoming_shows": len(upcoming_shows)
        }

        location_values["venues"].append(venue_data)
      
      response_data.append(location_values)

  except:
    db.session.rollback()    
    flash(" Please Try Again Later")
    return render_template("pages/home.html")
  
  finally:
    return render_template("pages/venues.html", areas=response_data)
  #return render_template('pages/venues.html', areas=data);
  # DONE: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searches = request.form.get("search_term", "")

  response = {"count" : 0, "data" : []}

  fields = ["id", "name"]

  search_results_venue = (
    db.session.query(Venue)
        .filter(Venue.name.ilike(f"%{searches}%"))
        .options(load_only(*fields))
        .all()
  )

  response["count"] = len(search_results_venue)

  for result in search_results_venue:
    result_item = {
      "id" : result.id,
      "name" : result.name
    }
    response["data"].append(result_item)
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = {}

  try:
    view_venue = Venue.query.get(venue_id)
    #view_venue = Venue.query.filter_by(venue_id=venue_ids).all()
    if view_venue is None:
      return not_found_error(404)

    genres = []
    for g in view_venue.genres:
      genres.append(g.genre)
    print(genres)
    shows = Show.query.filter_by(Venue_ID=venue_id)

    date_today = datetime.datetime.now()

    past_shows_info = shows.filter(Show.start_time < date_today)
    past_shows = []
    for show in past_shows_info:
      artist_info = Artist.query.get(show.artist_id)
      show_data = {
        "artist_id" : artist_info.id,
        "artist_name" : artist_info.name,
        "artist_image_link" : artist_info.image_link,
        "start_time" : str(show.start_time)
      }
    
    past_shows.append(show_data)

    upcoming_shows_info = shows.filter(Show.start_time >= date_today).all()
    upcoming_shows = []
    for show in upcoming_shows_info:
      artist_info = Artist.query.get(show.artist_id)
      show_data = {
        "artist_id" : artist_info.id,
        "artist_name" : artist_info.name,
        "artist_image_link" : artist_info.image_link,
        "start_time" : str(show.start_time)
      }
      upcoming_shows.append(show_data)

    data ={
      "id": view_venue.id,
      "name": view_venue.name,
      "genres": genres,
      "address": view_venue.address,
      "city": view_venue.city,
      "state": view_venue.state,
      "phone": view_venue.phone,
      "website": view_venue.website_link,
      "facebook_link": view_venue.facebook_link,
      "seeking_talent": view_venue.seeking_talent,
      "seeking_description": view_venue.seeking_description,
      "image_link": view_venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
  }

  except:
    flash("Please Try Again Later")
  
  finally:
    db.session.close()
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
    form = VenueForm(request.form)

    venue = Venue(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      address = form.address.data,
      phone = form.phone.data,
      facebook_link = form.facebook_link.data,
      website_link = form.website_link.data,
      genres = form.genres.data,
      seeking_description = form.seeking_description.data,
      seeking_talent = form.seeking_talent.data,
      image_link = form.image_link.data,
    )

    
    """ new_venue = Venue(
      name=name,
      city=city,
      state=state,
      address=address,
      phone=phone,
      facebook_link=facebook_link,
      website_link=website_link,
      seeking_description=seeking_description,
      seeking_talent=seeking_talent,
      image_link=image_link,
    )

    genres_in_venue = []
    for genre in genres:
      current_gen = Venue(genres=genre)
      current_gen.venue = new_venue
      genres_in_venue.append(current_gen)
    """
    db.session.add(venue)
    db.session.commit()

    #db.session.refresh(venue)
    #flash("Venue" + new_venue.name + " of City:" + new_venue.city + " was Listed in the List of Venues" )
  # on successful db insert, flash success
    #flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except Exception as err:
    flash('An error occured for: {0}.Error: {1}'.format(venue.name, err))
    db.session.rollback()
    #print(sys.exc_info())
    #flash("We encountered an error for Venue "+ request.form.get("name") +" it could not be listed")
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')

  finally:
    db.session.close()
    return render_template('pages/home.html')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>/DeleteVenue', methods=['DELETE'])
def delete_venue(venue_id):

  venue_name = Venue.query.get("venue_id").name
  try:
    venue_to_delete = db.session.query(Venue).filter(Venue.id == venue_id)
    venue_to_delete.delete()
    db.session.commit()

    flash("Venue named" + "was successfully deleted")

  except:
    db.session.rollback()
    print(sys.exc_info())
    return jsonify(
      {
        "errorMessage": "Something went wrong. Please try again."
      }
    )
  finally:
    db.session.close()
    return redirect(url_for("index"))
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  fields_name = ["id","name"]
  artists_data = db.session.query(Artist).options(load_only(*fields_name)).all()

  return render_template("pages/artists.html", artists=artists_data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_query = request.form.get("search_term")

  response={
    "count": 0,
    "data": []
  }

  fields_data = ["id","name"]
  artist_search =(
    db.session.query(Artist).filter(Artist.name.ilike(f"%{search_query}%"))
    .options(load_only(*fields_data))
    .all()
  )

  num_of_upcoming_shows = 0

  response["count"] = len(artist_search)

  for searches in num_of_upcoming_shows:
    item ={
      "id": searches.id,
      "name" : searches.name,
      "num_of_upcoming_shows" : num_of_upcoming_shows,
    }

    response["data"].append(item)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data1= {}

  try:
    request_artist = Artist.query.get(artist_id)

    if request_artist is None:
      return not_found_error(404)

    genres = []
    for item in request_artist:
      genres.append(item.genre)

    shows = Show.query.filter_by(artist_id=artist_id)

    date_today = datetime.datetime.now()

    past_shows_records = shows.filter(Show.start_time < date_today).all()

    past_shows = []

    for a_show in past_shows_records:
      venue = Venue.query.get(a_show.venue_id)
      show_values = {
        "venue_id" : venue.name,
        "venue_name" : venue.name,
        "venue_image_link" : venue.image_link,
        "start_time" : str( a_show.start_time),
      }

      past_shows.append(show_values)

      upcoming_shows_records = shows.filter(Show.start_time >= date_today).all()
      upcoming_shows = []
      for a_show in upcoming_shows_records:
        venue = Venue.query.get(a_show.venue_id)

        show_data ={
          "venue_id" : venue.id,
          "venue_name" : venue.name,
          "venue_id" : venue.image_link,
          "show_start_time" : str(a_show.start_time),
        }

        upcoming_shows.append(show_data)

      data = {
        "id": request_artist.id,
      "name": request_artist.name,
      "genres": genres,
      "address": request_artist.address,
      "city": request_artist.city,
      "state": request_artist.state,
      "phone": request_artist.phone,
      "website": request_artist.website_link,
      "facebook_link": request_artist.facebook_link,
      "seeking_venue": request_artist.seeking_venue,
      "seeking_description": request_artist.seeking_description,
      "image_link": request_artist.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
      }
    
  except:
    print(sys.exc_info())
    flash("Something Went Wrong. Please do Try Again!")

  finally:
    db.session.close()

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist  = {}

  try:
    request_artist = Artist.query.get(artist_id)
    
    if request_artist is None:
      return not_found_error(404)

    genres = []
    if len (request_artist.genres) > 0:
      for item in request_artist:
        genres.append(item.genre)

    artist={
      "id": request_artist.id,
      "name": request_artist.name,
      "genres": genres,
      "city": request_artist.city,
      "state": request_artist.state,
      "phone": request_artist.phone,
      "website": request_artist.website_link,
      "facebook_link": request_artist.facebook_link,
      "seeking_venue": request_artist.seeking_venue,
      "seeking_description": request_artist.seeking_description,
      "image_link": request_artist.image_link,
    }

  except:
    print(sys.exc_info())
    flash('Something is wrong, Please Try Again !')
    return redirect(url_for("index"))

  finally:
    db.session.close()

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    request_artist_to_update = Artist.query.get(artist_id)

    if request_artist_to_update is None:
      return not_found_error (404)


    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    genres = request.form.getlist('genres')
    seeking_description = request.form.get('seeking_description')
    seeking_venue = request.form.get('seeking_venue')
    image_link = request.form.get('image_link')
    
    request_artist_to_update.name = name
    request_artist_to_update.city = city
    request_artist_to_update.state = state
    request_artist_to_update.phone = phone
    request_artist_to_update.facebook_link = facebook_link
    request_artist_to_update.website_link = website_link 
    request_artist_to_update.seeking_description = seeking_description
    request_artist_to_update.seeking_venue = seeking_venue
    request_artist_to_update.image_link = image_link
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

    artist_genres = []
    for genre in genres:
      current_genre = Artist(genre=genre)
      current_genre.artist = request_artist_to_update
      artist_genres.append(current_genre)

    db.session.add(artist_genres)  
    db.session.commit()

    db.session.refresh(artist_genres)
    flash("The Artist "+ name + " was successfully Added" )

  except:
    db.session.rollback()
    print(sys.exc_info())
    flash("An error occurred for artist " + request.form.get("name"))
  
  finally:
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue={}
  try:
    request_venue_to_update = Venue.query.get(venue_id)

    if request_venue_to_update is None:
      return not_found_error (404)


    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    address = request.form.get('address')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    genres = request.form.getlist('genres')
    seeking_description = request.form.get('seeking_description')
    seeking_talent = request.form.get('seeking_talent')
    image_link = request.form.get('image_link')
    
    request_venue_to_update.name = name
    request_venue_to_update.city = city
    request_venue_to_update.state = state
    request_venue_to_update.phone = phone
    request_venue_to_update.address = address
    request_venue_to_update.facebook_link = facebook_link
    request_venue_to_update.website_link = website_link 
    request_venue_to_update.seeking_description = seeking_description
    request_venue_to_update.seeking_talent = seeking_talent
    request_venue_to_update.image_link = image_link
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

    venue_genres = []
    for genre in genres:
      current_genre = Artist(genre=genre)
      current_genre.artist = request_venue_to_update
      venue_genres.append(current_genre)

    db.session.add(venue_genres)  
    db.session.commit()

    db.session.refresh(venue_genres)
    flash("The Venue "+ name + " was successfully Added" )

  except:
    db.session.rollback()
    print(sys.exc_info())
    flash("An error occurred for artist " + request.form.get("name"))
  
  finally:
    db.session.close()
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    phone = request.form.get("phone")
    genres =request.form.getlist("genres")
    facebook_link = request.form.get("facebook_link")
    website_link = request.form.get("website_link")
    image_link = request.form.get("image_link")
    seeking_venue = request.form.get("seeking_venue")
    seeking_description = request.form.get("seeking_description")

    new_artist = Artist(
      name=name, city=city,state=state ,phone=phone, facebook_link=facebook_link, 
      website_link=website_link, image_link=image_link, seeking_venue=seeking_venue,
      seeking_description=seeking_description,
    )

    genres_for_artist = []
    for g in genres:
      current_g = Artist(genre=g)
      current_g.artist = new_artist
      genres_for_artist.append(current_g)

    db.session.add(new_artist)
    db.session.commit()


  except:
    db.session.rollback()
    flash("We experienced an error for Artist " + request.form.get("name"))

  finally:
    db.session.close()
    
  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = {}
  try:
    shows = Show.query.all()
    for show in shows:
      venue_id = show.venue_id
      artist_id = show.artist_id
      artist = Artist.query.get(artist_id)
      
      every_show_data ={
        "venue_id": venue_id,
        "venue_name": Venue.query.get(venue_id).name,
        "artist_id" : artist_id,
        "artist_image_link": artist.image_link,
        "artist_name": artist.name,
        "start_time" : str(show.start_time),
      }

      data.append(every_show_data)

  except:
    db.session.rollback()
    print(sys.exc_info())
    flash("Something was not right")

  finally:
    return render_template('pages/shows.html', shows=data)


"""
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]

  """


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  errors = {"artist_id_error":False, "venue_id_error":False}

  try:
    artist_id = request.form.get("artist_id")
    venue_id = request.form.get("venue_id")
    start_time = request.form.get("start_time")

    find_artist = Artist.query.get(artist_id)
    if find_artist is None:
      errors["artist_id_error":] = True

    find_venue = Venue.query.get(venue_id)
    if find_venue is None:
      errors["venue_id_error"] = True


    if find_venue is not None and find_artist is not None:
      another_show = Show(
        artist_id=find_artist.id,
        venue_id=find_venue.id,
        start_time=start_time,
      )

      db.session.add(another_show)
      db.session.commit()

      flash("You have scheduled the show by: " + find_artist.name)

  except:
    db.session.rollback()
    flash("Something went wrong. Try Again Letter!")

  finally:
    db.session.close()
  

  if errors["artist_id_error"] is True:
    flash(
      "No artist with Id: " +  request.form.get("artist_id") + " Found"
    )
  elif errors["venue_id_error"] is True:
    flash(
      "No venue with Id: " +  request.form.get("venue_id") + " Found"
    )
  #Enable CSRF Protection Global

  #class flask_wtf.csrf.CSRFProtect(app=none)
   
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
