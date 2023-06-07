# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, jsonify
from sqlalchemy import func

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# reflect an existing database into a new model
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################

app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    """Homepage"""
    return (
        f"Welcome to the Homepage<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return the JSON representation of precipitation data"""
    # Perform your query and conversion to a dictionary
    session = Session(engine)
    # Replace this with your code to retrieve the last 12 months of precipitation data
    query_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = query_date[0]  # Extract the date value from the query result

    # Calculate the date one year from the last date in the dataset
    last_year_date = dt.datetime.strptime(query_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores for the last 12 months
    results_last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date).all()
    results_last_year_dict = dict(results_last_year)

    # Return the JSON representation of the dictionary
    session.close()
    return jsonify(results_last_year_dict)

@app.route('/api/v1.0/stations')
def stations():
    """Return a JSON list of stations"""
    # Replace this with your code to retrieve the stations from the dataset
    # Perform your query to retrieve the list of stations
    # Get data of the column station of the DB Station
    session = Session(engine)
    query_station = session.query(Station.station)
    # Assign to a pandas dataframe
    df2 = pd.DataFrame(query_station, columns=['station'])
    #count number of stations
    station_list = [df2['station'].nunique()]
    
    

    # Return the JSON representation of the list
    session.close()
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return a JSON list of temperature observations"""
    # Perform your query to retrieve the temperature observations
    session = Session(engine)
    results_t = session.query(Measurement.date, Measurement.tobs)
    # Replace this with your code to retrieve the observations for the most-active station
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
                   filter(Measurement.station == 'USC00519281')   # Revisar si sí se tiene que filtar estación.
    temperature_data_dict = dict(temperature_data)

    # Return the JSON representation of the list
    session.close()
    return jsonify(temperature_data_dict)

@app.route('/api/v1.0/<start>')
def start_date(start):
    """Return a JSON list of temperature statistics for a specified start date"""
    # Perform your query to calculate the temperature statistics for the specified start date
    session = Session(engine)
    # Query the maximum date from the "Measurement" table
    last_date = session.query(func.max(Measurement.date)).scalar()

    # Convert the last date to a datetime object
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d').date()

    # Calculate the date one year ago from the last date
    last_year_date = last_date - dt.timedelta(days=365)

    # Query the temperature observations for the most active station within the last 12 months
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= last_year_date).all()


    # Replace this with your code to calculate TMIN, TAVG, and TMAX for the specified start date

# Perform your query to calculate the temperature statistics for the specified start date

    # Query the temperature statistics for the specified start date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    # Extract the temperature statistics from the query result
    tmin, tavg, tmax = temperature_stats[0]

    # Create a dictionary to hold the temperature statistics
    temperature_statistics = {
        'TMIN': tmin,
        'TAVG': tavg,
        'TMAX': tmax
    }

# Convert the dictionary to JSON and return the result
    return jsonify(temperature_statistics)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    """Return a JSON list of temperature statistics for a specified start-end range"""
    # Perform your query to calculate the temperature statistics for the specified start-end range
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()  
    # Replace this with your code to calculate TMIN, TAVG, and TMAX for the specified range
    # Extract the temperature statistics from the query result
    tmin, tavg, tmax = temperature_stats[0]

    # Create a dictionary to hold the temperature statistics
    temperature_statistics = {
        'TMIN': tmin,
        'TAVG': tavg,
        'TMAX': tmax
    }
    # Return the JSON representation of the statistics
    return jsonify(temperature_statistics)

if __name__ == '__main__':
    app.run()
