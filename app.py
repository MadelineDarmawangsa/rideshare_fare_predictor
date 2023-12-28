import numpy as np
from flask import Flask, request, jsonify, render_template
from math import radians, cos, sin, asin, sqrt
import pickle
import requests
import urllib.parse
from geopy.geocoders import Nominatim
import geocoder

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    pickup, dropoff, hour = request.form.values()

    geocoded_pickup = geocoder.bing(pickup, key='AiCLMz_5eRW1nKB5_jdTvGrFKOk-BTnhrvQ6stoLJi5_i-XqdcPLKT34fRCibkQU')
    pickup_coords = geocoded_pickup.json
    geocoded_dropoff = geocoder.bing(dropoff, key='AiCLMz_5eRW1nKB5_jdTvGrFKOk-BTnhrvQ6stoLJi5_i-XqdcPLKT34fRCibkQU')
    dropoff_coords = geocoded_dropoff.json

    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 
        return c * r

    distance = haversine(pickup_coords['lng'],pickup_coords['lat'],dropoff_coords['lng'],dropoff_coords['lat'])
    features = [[int(distance)]+[int(hour)]]
    prediction = model.predict(features)
    output = max(6.0,np.round(prediction[0], 2)[0])

    return render_template('index.html', prediction_text='Uber fare should be ${}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)