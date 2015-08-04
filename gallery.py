# all the imports
from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, send_file
import os, re
import getpicbykey
import getpicsbydate
import getrandompic
import getalldateswithpictures


# configuration
DEBUG = True

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

basedir = "/Users/rickard/Pictures"

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

#@app.route('/')
#def show_pictures():
#    pictures, dirs = get_files_and_subdirs_from(basedir)
#    return render_template('index.html', pictures=pictures, dirs=dirs)

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
        print "hej"
        key = request.args.get('key')
        fullpath = getpicbykey.main(key)[1]
        return send_file(fullpath, mimetype='image/jpeg')
    elif request.args.has_key('random'):
        print "da"
        fullpath = getrandompic.main()[1]
        print fullpath
        return send_file(fullpath, mimetype='image/jpeg')
    else:
        return send_file("/Users/rickard/Documents/repos/gallery/gtfo.jpg", mimetype='image/jpeg')

@app.route('/', methods=['GET'])
def get_calendar_view():
    if request.args:
        return render_template('calendar.html', dates=getalldateswithpictures.main(str(int(request.args.get('year'))+0)))
    else:
        return render_template('calendar.html', dates=getalldateswithpictures.main(2015))

@app.route('/get_date', methods=['GET'])
def get_date():
    pickeys = getpicsbydate.main(request.args['year'],request.args.get('month'),request.args.get('day'))
    
    return render_template('calendar-dateview.html', year=request.args.get('year'), month=request.args.get('month'), day=request.args.get('day'), keys=pickeys)

if __name__ == '__main__':
    app.run()