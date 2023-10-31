# Import the dependencies.
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables


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


@app.route("/")
def welcome():
    """Wellcome to my Climate Analysis!"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# this function helps to get the precipation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    def precipitation():
        prec_result = session.query(Measurement.date, Measurement.prcp).all()
        p_data = {date: prcp for date, prcp in prec_result}
        return jsonify(p_data)

# this function should display a list of the stations 
@app.route("/api/v1.0/stations")
def stations():
    stat_results = session.query(Station.station, Station.name).all()
    s_data = [{"station": station, "name": name} for station, name in stat_results]
    return jsonify(s_data)

#this helps to get data from the previous year of temperatures 
@app.route("/api/v1.0/tobs")
def tobs():
    ld = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    ld = dt.datetime.strptime(ld[0], '%Y-%m-%d')
    one_year_ago = ld - dt.timedelta(days=365)
    tob_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).all()
    t_data = [{"date": date, "tobs": tobs} for date, tobs in tob_results]
    return jsonify(t_data)

#this calculates the statistics of the temperatures of the starting dates 
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    data_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    tmin, tavg, tmax = data_start[0]
    return jsonify({"TMIN": tmin, "TAVG": tavg, "TMAX": tmax})

#this calculates the stats of temperatures of the ending dates 
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    data_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    tmin, tavg, tmax = data_end[0]
    return jsonify({"TMIN": tmin, "TAVG": tavg, "TMAX": tmax})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

#All of them are in JSON format 

