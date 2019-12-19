# Import Flask
import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import create_engine
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup                                #
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create app
app = Flask(__name__)


# Define routes
@app.route("/")
def welcome():
    """List api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/enddate<br/>"
)

# Precipitation
@app.route("/api/v1.0/precipitation")
def date():
    

    session = Session(engine)

    prcp_date = session.query(Measurement.date, Measurement.prcp).all()
  
    session.close()

    return jsonify(prcp_date)


# Stations
@app.route("/api/v1.0/station")
def stations():

   
    session = Session(engine)

    station_total = session.query(Measurement.station.distinct()).all()

    session.close()

    return jsonify(station_total)


# Temperatures last year
@app.route("/api/v1.0/tobs")
def temp():


    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
  
    prcp_12mo = session.query(Measurement.tobs).filter(Measurement.date > query_date).all()
   
    session.close()

    return jsonify(prcp_12mo)



# Temperatures using start date
@app.route("/api/v1.0/startdate")
def start():


    session = Session(engine)
    start_date = '2017-07-05'
    
    # Query
    max_tobs = (session.query(func.max(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    min_tobs = (session.query(func.min(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    avg_tobs = (session.query(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    
    session.close()

    all_temperatures = {
        "Maximum Temperature" : max_tobs,
        "Minimum Temperature": min_tobs,
        "Average Temperature": avg_tobs
    }

    return jsonify(all_temperatures)

# Temperatures using start date - end date
@app.route("/api/v1.0/enddate")
def end():
    
    
    session = Session(engine)
    start_date = '2017-07-05'
    end_date = '2017-07-15'
    
    # Query
    max_tobs_ = (session.query(func.max(Measurement.tobs))).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()
    min_tobs_ = (session.query(func.min(Measurement.tobs))).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()
    avg_tobs_ = (session.query(func.avg(Measurement.tobs))).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()

    session.close()

    all_temperatures_ = {
        "Maximum Temperature" : max_tobs_,
        "Minimum Temperature": min_tobs_,
        "Average Temperature": avg_tobs_
    }

    return jsonify(all_temperatures_)


if __name__ == "__main__":
    app.run(debug=True)