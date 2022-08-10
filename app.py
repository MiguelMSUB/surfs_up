#Import Dependendies
import datetime as dt
import numpy as np
import pandas as pd

# dependencies we need for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#To import the Flask dependency
from flask import Flask, jsonify

# We'll set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

#Now let's reflect the database into our classes.
Base = automap_base()

# reflect the database:
Base.prepare(engine, reflect=True)

#save our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to our database
session = Session(engine)

# #create a new Flask app instance
# #"Instance" is a general term in programming to refer to a singular version of something
app = Flask(__name__)

# We can define the welcome route using the code below:
@app.route("/")

#The next step is to add the routing information for each of the other routes. 
#For this we'll create a function, and our return statement will have f-strings as a reference to all of the other routes.
def welcome():
    return('''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#The next route we'll build is for the precipitation analysis. 
# This route will occur separately from the welcome route
@app.route("/api/v1.0/precipitation")

#Next, we will create the precipitation() function.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Build the stations route.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Our last route will be to report on the minimum, average, and maximum temperatures. 
# #However, this route is different from the previous ones in that we will have to provide both a starting and ending date.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)