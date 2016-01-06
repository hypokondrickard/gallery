from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, send_file, jsonify
from flask_restful import Resource, Api
from helpers import *
import os, re
import json

app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)
app.debug = True

#configuration
DEBUG = True
DATABASE = "/tmp/gallery.db"

@app.before_request
def before_request():
    g.db = sqlite3.connect(DATABASE)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

class Get_pics_by_year(Resource):
    def get(self, year):
        return jsonify(get_pics_by_year(year))

api.add_resource(Get_pics_by_year, '/get_pics_by_year/<string:year>')

class Get_pics_by_date(Resource):
    def get(self, year, month, day):
        return jsonify(get_pics_by_date(year,month,day))

api.add_resource(Get_pics_by_date, '/get_pics_by_date/<string:year>/<string:month>/<string:day>')

class Get_pic(Resource):
    def get(self, key):
        if key:
            fullpath = get_pic_by_key(key)[1]
            return send_file(fullpath, mimetype='image/jpeg')
        else:
            return send_file("static/gtfo.jpg", mimetype='image/jpeg')

api.add_resource(Get_pic, '/get_pic/<string:key>')

@app.route('/select', methods=['GET'])
def select_album():
    new_basedir = request.args.get('dir')
    if (new_basedir.count("/") > 0):
        return_dir = re.sub('/[^/]*$', '', new_basedir)
    else:
        return_dir = "/"

    pictures, dirs = get_files_and_subdirs_from(basedir+"/"+new_basedir)
    return render_template('index.html', pictures=pictures, dirs=dirs, basedir=new_basedir, returndir=return_dir)

@app.route('/get_image', methods=['GET'])
def get_image():
    if request.args.has_key('key'):
        key = request.args.get('key')
        fullpath = get_pic_by_key(key)[1]
        return send_file(fullpath, mimetype='image/jpeg')
    elif request.args.has_key('random'):
        fullpath = get_random()[1]
        return send_file(fullpath, mimetype='image/jpeg')
    else:
        return send_file("static/gtfo.jpg", mimetype='image/jpeg')

@app.route('/get_image_view/<primkey>')
def get_image_view(primkey):
    return render_template('picture.html', date=get_date_from_picture(primkey), picture=primkey, neighbors=get_neighboring_pics(primkey))

@app.route('/', defaults={'year': None})
@app.route('/<year>')
def get_calendar(year):
    years_available = get_available_years()
    most_recent_year = years_available[-1]

    if year is None:
        return render_template('calendar.html', years=years_available, dates=get_calendar_data(most_recent_year))
    else:
        return render_template('calendar.html', years=years_available, dates=get_calendar_data(year))

@app.route('/<year>/<month>/<day>', methods=['GET'])
def get_date(year,month,day):
    pickeys = get_pics_by_date(year,month,day)

    first_picture = pickeys[0]
    first_picture_neighbors = get_neighboring_pics(first_picture)
    last_picture_previous_date = first_picture_neighbors[0]
    previous_date = get_date_from_picture(last_picture_previous_date)
    
    last_picture = pickeys[-1]
    last_picture_neighbors = get_neighboring_pics(last_picture)
    first_picture_next_date = last_picture_neighbors[1]
    next_date = get_date_from_picture(first_picture_next_date)

    return render_template('calendar-dateview.html', year=year, month=month, day=day, keys=pickeys, next_date=next_date, previous_date=previous_date)

if __name__ == '__main__':
    app.run(host='0.0.0.0')