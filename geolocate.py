import urllib.request
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/') # FIX THIS
def index_page():
    return render_template('index.html')

@app.route('/location/', methods=['POST', 'GET'])
def result_page():
    search = request.form['location']
    search_results = search_location(search)
    if search_results == None:
        return render_template('index.html')

    results = search_results
    results['search'] = search.upper()
    # results['faddress'] = search_results['formatted_address']
    # results['lat'] = search_results['geometry']['location']['lat']
    # results['lng'] = search_results['geometry']['location']['lng']
    return render_template('result.html', results=results)

@app.route('/about/')
def about_page():
    return render_template('about.html')


# App logic for the google-geo api

def search_location(user_search):
    geojson_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    address = user_search
    if len(address) < 1 :
        return None

    url = geojson_url + urllib.parse.urlencode({'sensor':'false', 'address':address}) #http://maps.googleapis.com/maps/api/geocode/json
    geojson = urllib.request.urlopen(url)
    print("Retrieving ", geojson.geturl()) # delete when finished
    data = geojson.read()
    print("Retrieved ", len(data), " characters") # delete when finished

    try:
        info = json.loads(data)
    except:
        return None

    if 'status' not in info or info['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        return None

    # print(json.dumps(info, indent=4))
    results = {}
    results['faddress'] = info['results'][0]['formatted_address']
    results['lat'] = info['results'][0]['geometry']['location']['lat']
    results['lng'] = info['results'][0]['geometry']['location']['lng']
    return results
