
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


enigine = create_engine("sqlite:///hawaii.sqlite")

# I know I need this, but dont know what it does
Base = automap_base()

Base.prepare(enigine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(enigine)


app = Flask(__name__)


@app.route("/")
#List all available routes
def welcome ():
	return (
		f"Welcome to the Hawii Weather API<br>"
		f"Available Routes:<br>"
		f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/<start><br>"
		f"/api/v1.0<start>/<end><br>"
	)    


@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return the precip data as json"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query ( Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    precipitation= {date:prcp for date,prcp in results}
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
#         """"Return station data as json""""
    stations = session.query(Station.station).all()
    results = list(np.ravel(stations))
    return jsonify(results)
    
@app.route("/api/v1.0/tobs")
def tobs():
#             """tobs data as json"""
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23", Measurement.station == "USC00519281").all()
    results_tobs = list(np.ravel(tobs))
    return jsonify(results_tobs)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")      
def start_end(start=None, end=None): 
    if not end:
        
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        
        results =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        #session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == start).all()
        temp= list(np.ravel(results))
        return jsonify(temp)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    results =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start).all()

    
#    session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) >=start).filter(func.strftime("%m-%d", Measurement.date) <=end ).all()
    temp= list(np.ravel(results))
    return jsonify(temp)


 #   return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()





if __name__ == "__main__":
    app.run(debug=True)