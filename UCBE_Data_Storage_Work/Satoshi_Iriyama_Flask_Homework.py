import numpy as np
import datetime as dt
import pandas as pd
from datetime import datetime

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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Calculate the date 1 year ago from today
last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).\
        filter(Measurement.station == "USC00519281").filter(Measurement.date >= last_year_date).order_by(Measurement.date).all()

    all_dates_data = []

    for date_data in results:
        date_data_dict = {}
        date_data_dict["date"] = date_data.date
        date_data_dict["precipitation"] = date_data.prcp
        all_dates_data.append(date_data_dict)

    return jsonify(all_dates_data)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station).all()

    all_stations = []

    for station_data in results:
        station_dict = {}
        station_dict["station"] = station_data.station
        station_dict["name"] = station_data.name
        all_stations.append(station_dict)
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperature():
    results = session.query(Measurement).\
        filter(Measurement.station == "USC00519281").filter(Measurement.date >= last_year_date).order_by(Measurement.date).all()

    all_dates_data = []

    for date_data in results:
        date_data_dict = {}
        date_data_dict["date"] = date_data.date
        date_data_dict["temperature"] = date_data.tobs
        all_dates_data.append(date_data_dict)

    return jsonify(all_dates_data)


@app.route("/api/v1.0/<start>")
def averages(start):
    TMIN = session.query(func.min(Measurement.tobs)).filter(func.strftime("%m-%d", Measurement.date) == start).first()[0]
    TAVG = session.query(func.avg(Measurement.tobs)).filter(func.strftime("%m-%d", Measurement.date) == start).first()[0]
    TMAX = session.query(func.max(Measurement.tobs)).filter(func.strftime("%m-%d", Measurement.date) == start).first()[0]
    data_dic = {"TMIN": TMIN,
                "TAVG": TAVG,
                "TMAX": TMAX}

    return jsonify(data_dic)



@app.route("/api/v1.0/<start>/<end>")
def averages_2(start, end):

    start_md = datetime.strptime(start, '%m-%d')
    end_md = datetime.strptime(end, '%m-%d')
    
    datelist= []

    date = start_md - dt.timedelta(days=1)

    while date < end_md :
        date = date + dt.timedelta(days=1)
        datelist.append(date)

    # Stip off the year and save a list of %m-%d strings
    datelist_md = [date.strftime("%m-%d") for date in datelist]
    datelist_md

    data_dic_list = [] 

    for date in datelist_md:
        TMIN = session.query(func.min(Measurement.tobs)).filter(func.strftime("%m-%d", Measurement.date) == date).first()[0]
        TAVG = session.query(func.avg(Measurement.tobs)).filter(func.strftime("%m-%d", Measurement.date) == date).first()[0]
        TMAX = session.query(func.max(Measurement.tobs)).filter(func.strftime("%m-%d", Measurement.date) == date).first()[0]
        data_dic = {"Date": date,
                    "TMIN": TMIN,
                    "TAVG": TAVG,
                    "TMAX": TMAX}

        data_dic_list.append(data_dic)

    return jsonify(data_dic_list)


if __name__ == '__main__':
    app.run(debug=True)

