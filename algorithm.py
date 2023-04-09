import os
from aiohttp import Fingerprint
import cv2
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


# test_image_input = "./socofing/socofing/SOCOFing/Real/1__M_Left_index_finger.BMP"
# The application is now picking from the web application

# This is the directory to the Socofing real dataset
real_fingerprint_directory = "./socofing/socofing/SOCOFing/Real"

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "bmp"}

app = Flask(__name__)
app.secret_key = str(os.urandom(30)) + 'AGSNsdjWuWyrwiur&7a72464642462646'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# The helps in the allowed filetypes
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def search(test_image_input):
    fingerprint_image_to_search = cv2.imread(test_image_input)

    best_score = counter = 0
    filename = image = kp1 = kp2 = mp = None

    for file in os.listdir(real_fingerprint_directory):
        if counter % 10 == 0:
            print(counter)
            print(file)
        counter += 1

        fingerprint_img = cv2.imread(real_fingerprint_directory + "/" + file)
        sift = cv2.SIFT_create()
        keypoints_1, des1 = sift.detectAndCompute(fingerprint_image_to_search, None)
        keypoints_2, des2 = sift.detectAndCompute(fingerprint_img, None)
        # print(kp1, des1)
        # print(kp2, des2)
        # print(len(kp1), len(kp2))
        # print(len(des1), len(des2))
        # print(des1[0], des2[0])\
        # fast library for approx best match KNN
        matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(
            des1, des2, k=2
        )

        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = 0
        if len(keypoints_1) <= len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)
        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = file
            image = fingerprint_img
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    print("Best match:  " + filename)
    print("Best score:  " + str(best_score))

    if len(match_points) > 0:
        result = cv2.drawMatches(fingerprint_image_to_search, kp1, image, kp2, mp, None)
        result = cv2.resize(result, None, fx=5, fy=5)
        cv2.imshow("Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return filename, best_score


@app.route("/")
def index(results=None):
    return render_template("index.html", results=results)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results = search(os.path.join(UPLOAD_FOLDER,filename))
            return render_template("index.html", results=results)
    
    return render_template('uploads.html')
  

if __name__ == "__main__":
    app.run(debug=True)
