# Import the Flask Dependency
from flask import Flask
from flask import jsonify

# import all the other dependancies
import datetime as dt
import numpy as np
import pandas as pd

# import all dependancies we need for SQLAlchemy
# this will help us access our data in the SQLite database.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Set Up the Database
# Access the SQLite database.
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes.
Base = automap_base()

# use python flask function will you use to reflect the tables
# to help keep our code separate
Base.prepare(engine, reflect=True)

# Reference the measurement class 
Measurement = Base.classes.measurement
# Reference the station class 
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)


# Create a New Flask App Instance
# aka, define our Flask app,
# This will create a Flask application called "app."
app = Flask(__name__)


#       ___       __   __         ___     __   __       ___  ___ 
# |  | |__  |    /  ` /  \  |\/| |__     |__) /  \ |  |  |  |__  
# |/\| |___ |___ \__, \__/  |  | |___    |  \ \__/ \__/  |  |___ 


# create flask routes
# define the starting point, also known as the root.
# aka, define what to do when a user goes to the index route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
    
# type: "python3 app.py" in terminal
# copy paste http link into web browser

# Note:
# When creating routes, follow the naming convention /api/v1.0/ 
# followed by the name of the route. 
# This convention signifies that this is version 1 of our application.


#  __   __   ___  __     __    ___      ___    __           __   __       ___  ___ 
# |__) |__) |__  /  ` | |__) |  |   /\   |  | /  \ |\ |    |__) /  \ |  |  |  |__  
# |    |  \ |___ \__, | |    |  |  /~~\  |  | \__/ | \|    |  \ \__/ \__/  |  |___ 


# Build the next route for the precipitation analysis.
@app.route("/api/v1.0/precipitation")

# create the precipitation() function.
def precipitation():
    # calculate the date one year ago from the most recent date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # write a query to get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all() 
        # note: ".\" signifies that we want our query to continue on the next line.
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
    # note: use jsonify() to format our results into a JSON structured file.
    

#  __  ___      ___    __        __      __   __       ___  ___ 
# /__`  |   /\   |  | /  \ |\ | /__`    |__) /  \ |  |  |  |__  
# .__/  |  /~~\  |  | \__/ | \| .__/    |  \ \__/ \__/  |  |___ 


# Build the next route for the stations analysis.
@app.route("/api/v1.0/stations")

# create the stations() function.
def stations():
    # create a query that will allow us to get all of the stations in our database.
    results = session.query(Station.station).all()
    # unraveling our results into a one-dimensional array. 
    # use the function np.ravel(), with results as our parameter.
    # convert our unraveled results into a list.
    stations = list(np.ravel(results))
    return jsonify(stations) # jsonify the list and return it as JSON.


#       __       ___                  ___  ___        __   ___  __       ___       __   ___     __   __       ___  ___ 
# |\/| /  \ |\ |  |  |__| |    \ /     |  |__   |\/| |__) |__  |__)  /\   |  |  | |__) |__     |__) /  \ |  |  |  |__  
# |  | \__/ | \|  |  |  | |___  |      |  |___  |  | |    |___ |  \ /~~\  |  \__/ |  \ |___    |  \ \__/ \__/  |  |___ 


# Build the next route for the temperature observations.
@app.route("/api/v1.0/tobs")

# create the temp_monthly() function.
def temp_monthly():
    # calculate the date one year ago from the last date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # use the function np.ravel(), with results as our parameter.
    # convert our unraveled results into a list.
    temps = list(np.ravel(results))
    return jsonify(temps)


#  __  ___      ___    __  ___    __   __      __   __       ___  ___ 
# /__`  |   /\   |  | /__`  |  | /  ` /__`    |__) /  \ |  |  |  |__  
# .__/  |  /~~\  |  | .__/  |  | \__, .__/    |  \ \__/ \__/  |  |___ 


# create a route for our summary statistics report.
    # this route is different from the previous ones
    # in that we will have to provide both a starting and ending date.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


# calculate the temperature minimum, average, and maximum with the start and end dates.
# use the sel list, which is simply the data points we need to collect.
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


if __name__ == "__main__":
    app.run(debug=True)