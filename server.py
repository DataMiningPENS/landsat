from flask import Flask, url_for, send_from_directory, request, render_template
import logging, os
from werkzeug import secure_filename
from lib.ImageProcess import ImageProcess as ip
import cv2

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/static/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

image_name = []

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/upload', methods = ['POST'])
def api_root():
    global image_name
    image_name.append(request.files['image'].filename)
    
    app.logger.info(PROJECT_HOME)
    if(request.method == 'POST' and request.files['image']):
    	app.logger.info(app.config['UPLOAD_FOLDER'])
    	img = request.files['image']
    	img_name = secure_filename(img.filename)
    	create_new_folder(app.config['UPLOAD_FOLDER'])
    	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    	app.logger.info("saving {}".format(saved_path))
    	img.save(saved_path)
    	if(send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)):
            return img_name
    else:
    	return "Where is the image?"

@app.route('/cluster-lib', methods = ['POST'])
def cluster_lib():
    img = ip.load_image(image_name)
    data, cluster = ip.convert_index(image_name, img)
    json = request.form['num-cluster']
    cluster = ip.clustering_lib(data, img, int(json))
    final = ip.generate_image(cluster, img, int(json))
    # print(cluster)
    return final+'.png'

@app.route('/')
def upload_file():
   return render_template('test.html')

@app.route('/coba')
def coba1():
    ip.coba()


if __name__ == '__main__':
    app.run(host='localhost', debug=False)