from flask import Flask, render_template,flash,request,redirect,url_for
################
import os
from werkzeug.utils import secure_filename
###############
app = Flask(__name__)
###############
@app.route('/')
def home():
   return render_template('readmybook.html')
@app.route('/imgtxt',methods=['GET','POST'])

def imgtxt():
   return render_template('imagetovoice.html')
###############
#to link back button
@app.route('/back',methods=['get','post'])
def back():
    return render_template("readmybook.html")
########

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('imagetovoice.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
   app.run(debug=True,port=5000)
