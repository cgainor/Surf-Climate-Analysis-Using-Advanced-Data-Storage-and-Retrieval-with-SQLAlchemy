import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Stations = Base.classes.station
Measurements = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of all date/precipitation key pairs"""
    # Query all data
    results = session.query(Measurements.date, Measurements.prcp).all()

    # Convert list of tuples into normal list
    all_precip = []
    for date, precipitation in results:
        precip_dict = {}
        precip_dict[date] = precipitation
        all_precip.append(precip_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""
    # Query all data
    results = session.query(Stations.station, Stations.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of tobs from the dataset"""
    # Find date of one year before last data point
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_12_months = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date() - dt.timedelta(days=365)

    # Query all data
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= last_12_months).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_only(start):
    """Return a json list of tobs from the dataset"""
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range.
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).all()

    # Convert list of tuples into normal list
    start_tobs = list(np.ravel(results))

    return jsonify(start_tobs)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a json list of tobs from the dataset"""
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    # Convert list of tuples into normal list
    start_end_tobs = list(np.ravel(results))

    return jsonify(start_end_tobs)


if __name__ == '__main__':
    app.run(debug=True)