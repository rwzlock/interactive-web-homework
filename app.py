# import necessary libraries
import numpy as np
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)


#Bellybutton table containing columns for all the data in the
#samples_metadata table from the database
class Bellybutton(db.Model):
    __tablename__ = 'samples_metadata'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String) #collection event
    ethnicity = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    wfreq = db.Column(db.Integer) #washing frequency
    bbtype = db.Column(db.String)
    location = db.Column(db.String)
    country012 = db.Column(db.String)
    zip012 = db.Column(db.Integer)
    country1319 = db.Column(db.String)
    zip1319 = db.Column(db.Integer)
    dog = db.Column(db.String)
    cat = db.Column(db.String)
    impsurface013 = db.Column(db.Integer) #Impervious surface
    npp013 = db.Column(db.Float) #Net Primary Productivity
    nmaxtemp013 = db.Column(db.Float) #Mean maximum monthly temp
    pfc013 = db.Column(db.Float) #Percentage forest cover
    impsurface1319 = db.Column(db.Integer)
    npp1319 = db.Column(db.Float)
    nmaxtemp1319 = db.Column(db.Float)
    pfc1319 = db.Column(db.Float)

    def __repr__(self):
        return '<Bellybutton %r>' % (self.id)

#Tables in SQLITE Database - samples, samples_metadata, otu

#################################################
# Routes
#################################################

# Create database tables
@app.before_first_request
def setup():
    # Connect table to our server
    db.create_all()

@app.route("/")
def index():
    """Return the dasboard hompage"""
    return render_template('index.html')

@app.route("/names")
def sample_name_data():
    """Return Belly Button collection events"""

    # query for the sample names (Wronge Table)
    names = db.session.query(Bellybutton.event).all()

    return jsonify(names)

@app.route("/otu")
def otu_data():
    """List of OTU descriptions"""

    otu_df = pd.read_csv("DataSets\belly_button_biodiversity_otu_id.csv", columns=['id', 'description'])
    # query for the sample names
    otu_list = otu_df['description'].values.tolist()

    return jsonify(otu_list)

@app.route('/metadata/<sample>')
def metadata_sample(event):
    """MetaData for a given sample"""

    results = db.session.query(Bellybutton.age,
                               Bellybutton.bbtype,
                               Bellybutton.ethnicity,
                               Bellybutton.gender,
                               Bellybutton.location,
                               Bellybutton.id).\
                               filter(Bellybutton.event==event).all()

    age = [result[0] for result in results]
    bbtype = [result[1] for result in results]
    ethnicity = [result[2] for result in results]
    gender = [result[3] for result in results]
    location = [result[4] for result in results]
    sampleid = [result[5] for result in results]

    # Generate the plot trace
    sample_trace = {
        "AGE": age,
        "BBTYPE": bbtype,
        "ETHNICITY": ethnicity,
        "GENDER": gender,
        "LOCATION": location,
        "SAMPLEID": sampleid
        #"type": "bar"
    }
    return jsonify(sample_trace)

@app.route('/wfreq/<sample>')
def wfreq_sample(event):
    """Washing Frequency for a given sample"""

    sample_wfreq = db.session.query(Bellybutton.wfreq).\
                               filter(Bellybutton.event==event).all()

    return jsonify(sample_wfreq)

if __name__ == "__main__":
    app.run()
