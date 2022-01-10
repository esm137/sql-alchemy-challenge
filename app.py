import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = engine = create_engine("sqlite:///Resources/hawaii.sqlite")

app = Flask(__name__)


Base = automap_base()
Base.prepare(engine, reflect=True)
measurement=Base.classes.measurement
station=Base.classes.station
session = Session(engine)

@app.route('/')
def welcome():
    return(f'routes:<br/>'
            f'/api/v1.0/precipitation<br/>'
            f'/api/v1.0/stations<br/>'
            f'/api/v1.0/tobs<br/>'
            f'/api/v1.0/<start><br/>'
            f'/api/v1.0/<start>/<end><br/>'

    )



@app.route('/api/v1.0/precipitation')
def percipitation():
    
    query=pd.DataFrame(engine.execute('select date,prcp from measurement where date>="2016-08-23" order by date desc;').fetchall())
    
    return(
       
       query.to_json()

    )



@app.route('/api/v1.0/stations')
def stations():
    
    query=pd.DataFrame(engine.execute('select station from measurement').fetchall())
    return(
       
       query.to_json()

    )


@app.route('/api/v1.0/tobs')
def tobs():
    query=pd.DataFrame(engine.execute('select tobs from measurement where station="USC00519281" and date>="2016-08-23"').fetchall())
    
    return(
       query.to_json()
       

    )





@app.route('/api/v1.0/<start>')
def start(start):
    
    query=pd.DataFrame(engine.execute(f'select min(tobs) ,max(tobs) ,avg(tobs)  from measurement where date>={start}'))
    return(
       query.to_json()
       

    )

@app.route('/api/v1.0/<start>/<end>')
def startend(start,end):
    query=pd.DataFrame(engine.execute(f'select min(tobs),max(tobs),avg(tobs) from measurement where date>={start} and date<={end}'))
    
    return(
       
       query.to_json()

    )


if __name__ == '__main__':
    app.run(debug=True)