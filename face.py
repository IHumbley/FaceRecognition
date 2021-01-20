'''
PROGRAMMER: Matin Kahi
DESCRIPTION:
this flask api recognition the admin faces to login 

if picture face exist in `pictureDatabse` folder api return `{'ok':True, 'result':'Welcome To Panel Admin.'}` 
else we return false

REQUIREMENTS: flask, face_recognition, os , time
- pip3 install face_recognition  
- pip3 install Flask

GITHUB: https://github.com/MrSubmissive
'''

import face_recognition, os, time
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def detection(photo_path) -> bool:
	admin_photo = []
	for filename in os.listdir('pictureDatabse'):
		img = os.path.isfile(os.path.join('pictureDatabse', filename))
		if img:
			try:
				photo = face_recognition.load_image_file(os.path.join('pictureDatabse', filename))
				photo = face_recognition.face_encodings(photo)[0]
				admin_photo.append(photo)
			except OSError:
				pass
	lock = face_recognition.load_image_file(photo_path)
	lock = face_recognition.face_encodings(lock)[0]
	
	res = face_recognition.compare_faces(admin_photo, lock)
	for i in res:
		if i == True:
			return True
	return False

def allowed_file(filename) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        if 'file' not in request.files:
            status = {'ok':False, 'result':'no file part'}
		os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(status)
        file = request.files['file']
        if file.filename == '':
            status = {'ok':False, 'result':'no selected file'}
		os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(status)
        if file and allowed_file(file.filename):
            filename = str(time.time()) + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if detection(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                status = {'ok':True, 'result':'Welcome To Panel Admin.'}
                os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return jsonify(status)
            else:
                status = {'ok':False, 'results':'Heyyyy You Are Not Admin.'}
                os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return jsonify(status)
        elif not allowed_file(file.filename):
            status = {'ok':False, 'result':'invalid file format. we can acept PNG JPG JPEG'}
            return jsonify(status)
    return '''
    <!doctype html>
    <title>Face recognition</title>
    <h1>Upload Face</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept="image/*">
      <input type=submit value=Upload>
    </form>
    '''


app.run(debug=True) # if you want you can change debug mode
