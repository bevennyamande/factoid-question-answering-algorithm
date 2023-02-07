import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from fingerprint_matching import algorithm

app = Flask(__name__)
app.secret_key = os.urandom(34)

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'temp')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    # find the file in the request parameter and process to the folder containing the fingerprints
    # also engage the algorithm here
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file = request.files['filename']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
## you call your algorithm here 
        #algorithm(file)


        # file has been uploaded now you can call your algorithm here and
        #  after processing return the user to a desirable page

        return redirect(url_for('index'))

    if __name__ == "__main__": 
        app.run(debug=True)
