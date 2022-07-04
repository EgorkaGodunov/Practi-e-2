import matplotlib.pyplot as plt
import string
import numpy as np
import matplotlib
import random
import matplotlib.pylab as pylab
from PIL import ImageOps, Image
from datetime import timedelta, datetime
import os
from flask import Flask, render_template, request,redirect,send_from_directory,url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from pyexcel_xls import save_data

x = np.arange(0,10)
for i in range(10):
    y = random.randrange(1,9)
ys1= [5,6,5,8,7,9,9,7,5,6]
coords=[]
plt.plot(x,ys1)



_f = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
fname = _f+'.'+'png'
plt.savefig('graphs/'+fname,dpi=100)
def get_colors(pth):
    colors={}
    img = Image.open(pth)
    pix = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i,j][:-1] not in colors and pix[i,j][:-1]!=(255,255,255) and 100<i<500 and 100<j<300:
                colors[pix[i,j][:-1]]=1
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i,j][:-1] in colors:
                colors[pix[i,j][:-1]]+=1
    s=dict(sorted(colors.items(), key=lambda item: item[1])[-1:])
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i,j][:-1] == list(s.keys())[0]:
                if pix[i,j][:-1] == list(s.keys())[0]:
                    if [i,j] not in coords:
                        coords.append([i,j])
    return coords





app = Flask(__name__)
tr='Plot Digitazer'
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
plot_name=[]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html',title=tr)


@app.route("/upload", methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if(len(plot_name)<2):
                plot_name.append(filename)
#             print(plot_name)
            return render_template('index.html',link=url_for('uploaded_file',filename=filename))
    return index()
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route("/plot_selection", methods=['POST','GET'])
def plot_selection():
    if request.method=='POST':
        plot_type = request.form['plot']
        colors = request.form['colors'].split(',')
        points = request.form['points'].split(',')

#         print(plot_type)
        arr_colors=[]
        for i in range(len(colors)):
            if i % 3 == 0:
                arr_colors.append((int(colors[i-2]),int(colors[i-1]),int(colors[i])))
#         print(arr_colors)
        arr_points=[]
        for i in range(len(points)):
            if i % 2 == 0:
                arr_points.append([points[i-1],points[i]])
#         print(arr_points)
#         print(plot_name)
        if plot_type=='xyplot':
            s=get_colors(pth='uploads/'+plot_name[0])
            print(s)
            _f = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            fname = _f+'.'+'xls'
            save_data(fname,s)
        return render_template('index.html')
if __name__ == "__main__":
    #Wi-Fi ------------   192.168.0.103
    #Точка доступа ----   192.168.43.58
    app.run(host='192.168.0.103', port=9000, debug=False)