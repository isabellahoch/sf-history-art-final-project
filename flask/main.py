from flask import Flask, render_template, request, redirect, url_for, make_response, abort

try:
	# for internal server
	from urlparse import urlparse, urljoin
except:
	# for heroku push:
	from urllib.parse import urlparse, urljoin

from math import ceil
import random
import json
import os
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

strava_code = "5300aa6b7e3aa9996f9505cd520a205eedd79b96"
strava_code = "ef68cbad0ee3a6d0bf644a03d60207ee5df3c014"

import requests
import json

from data import landmark_data

def get_info():
	info = {}
	info["sources"] = []
	info["sources"].append({"name":"Strava San Francisco Running Guide","website":"https://www.strava.com/local/us/san-francisco/running"})
	info["sources"].append({"name":"SF Running Clubs","website":"https://thebolditalic.com/sf-running-clubs-the-bold-italic-san-francisco-5c5a064901f9?gi=b827521bf1e1"})
	# info["sources"].append({"name":"DataSF COVID-19 Data and Reports","website":"https://data.sfgov.org/stories/s/fjki-2fab"})
	# info["sources"].append({"name":"Send a Virtual Hug","website":"http://sendavirtualhug.com"})
	return info

@app.errorhandler(404)
def page_not_found(e):
    title = 'Not Found'
    code = '404'
    message = "We can't seem to find the page you're looking for."
    return render_template('error.html', code = code, message = message, title = title, info = get_info()), 404

@app.errorhandler(403)
def page_forbidden(e):
    title = 'Forbidden'
    code = '403'
    message = "You do not have access to this page."
    return render_template('error.html', code = code, message = message, title = title, info = get_info()), 403

@app.errorhandler(500)
def internal_server_error(e):
    title = 'Internal Server Error'
    code = '500'
    message = "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    return render_template('error.html', code = code, message = message, title = title, info = get_info()), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    info = get_info()
    info["landmarks"] = landmark_data
    return render_template('index.html', info=info)

@app.route('/map')
def map():
	info = get_info()
	return render_template('map.html', info=info)

@app.route('/bibliography')
def bibliography():
	info = get_info()
	return render_template('bibliography.html', info=info)

@app.route('/landmarks')
def landmarks():
    info = get_info()
    info["landmarks"] = landmark_data
    return render_template('landmarks.html', info=info)

@app.route('/about')
def about():
    info = get_info()
    return render_template('about.html', info=info)

@app.route('/scenic-runs')
def scenic_runs():
	info = get_info()
	info['runs_unformatted'] = [{'title':'Great Highway Beach Run','code':"<iframe height='405' width='590' frameborder='0' allowtransparency='true' scrolling='no' src='https://www.strava.com/activities/4371053769/embed/199dd2f7bd75477bdfffe4d571016ece3549c411'></iframe>"},{'title':'Lands End, Presidio, & Golden Gate Park Loop', 'code':"<iframe height='405' width='590' frameborder='0' allowtransparency='true' scrolling='no' src='https://www.strava.com/activities/4638177056/embed/14460d1cbe1ad550699d8a89d64ae472f2300591'></iframe>",'iframe':'https://www.strava.com/activities/4638177056/embed/14460d1cbe1ad550699d8a89d64ae472f2300591'},{'title':"Fisherman's Wharf Scenic Run", 'code':"<iframe height='405' width='590' frameborder='0' allowtransparency='true' scrolling='no' src='https://www.strava.com/activities/3189891628/embed/c188ceabe8fe054da7ee46c69d33a79a0f5b4c69'></iframe>",'iframe':'https://www.strava.com/activities/3189891628/embed/c188ceabe8fe054da7ee46c69d33a79a0f5b4c69'}]
	info['runs'] = []
	for run in info['runs_unformatted']:
		this_run = run
		this_run['iframe'] = run['code'].split("src='")[1].split("'")[0]
		info['runs'].append(this_run) 
	return render_template('my_runs.html', info=info)

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml """
    pages = []
    # All pages registed with flask apps
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(rule.rule)

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    # return response
    return render_template('sitemap_template.xml', pages=pages)



app.jinja_env.cache = {}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)