from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, send_file
from helpers import *
import os, re

app = Flask(__name__)
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

def get_files_and_subdirs_from(workingdir):
    if os.path.isdir(workingdir) & (os.path.abspath(workingdir) == workingdir):
        dirs = []
        files = []
        for item in os.listdir(workingdir):
            itempath = os.path.join(workingdir,item)
            if os.path.isdir(itempath):
                dirs.append(item)
            elif os.path.isfile(itempath):
                files.append(item)
        return files, dirs
    else:
        return [os.path.abspath(workingdir)], [workingdir]  

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

@app.route('/', methods=['GET'])
def get_calendar_view():
    if request.args:
        return render_template('calendar.html', dates=get_calendar(str(int(request.args.get('year'))+0)))
    else:
        return render_template('calendar.html', dates=get_calendar(2015))

@app.route('/get_date', methods=['GET'])
def get_date():
    #pickeys = get_pics_by_date(request.args['year'],request.args.get('month'),request.args.get('day'))
    pickeys = get_pics_by_timestamp(request.args['year'],request.args.get('month'),request.args.get('day'))
    
    return render_template('calendar-dateview.html', year=request.args.get('year'), month=request.args.get('month'), day=request.args.get('day'), keys=pickeys)

if __name__ == '__main__':
    app.run(host='0.0.0.0')