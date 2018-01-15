import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from flask_sqlalchemy import SQLAlchemy

names = ['ali Siddiqui', 'hamza Siddiqui', 'hammad ali siddiqui', 'ghaffar', 'siddiqui ali', 'sana siddiqui']

app = Flask(__name__)                                                                                                                  #
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'Roman Rogers'

app.config['UPLOADED_FILES_ALLOW'] = set(['png', 'jpg', 'jpeg','jfif', 'pdf','txt'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///upload.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'Static/Uploaded_Files'                                                    #Image destination
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])                      #Allowed Format
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

f = open('Upload Files.txt','w')                                                           #Saving Uploaded files lisr in text file

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    def __init__(self, content):
        self.content = content
        self.priority = False

    def __repr__(self):
        return '<Content %s>' % self.content
db.create_all()

################################     API 1      ##################################

def allowed_file(filename):                                                                #Just a function who returns TRUE if extension in in the list
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/API-1', methods=['GET', 'POST'])
def upload_file():

    tasks = Task.query.all()
   
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file'] 
        
        if file.filename == '':                         # if user does not select file, browser also submit a empty part without filename
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            content = filename
            task = Task(content)
            db.session.add(task)
            db.session.commit() 
            f = open('Upload Files.txt','a')           # Opening text file
            f.write('\n'+' API-1* '+filename)           # Saving uploaded file name with extension
            f.close()                                 # Closing the text file
        return redirect(url_for('uploaded_file', filename=filename)), lastname(names)
    return '''
    <!doctype html>
    <title>Upload New File</title>  
    <h1>Upload New File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/Upload-API/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

###########################     API 2     ##########################

app.config['UPLOADED_FILES_ALLOW'] = set(['png', 'jpg', 'jpeg','jfif', 'pdf','txt'])
app.config['UPLOADED_FILES_DEST'] = 'Static/Uploaded_Files'
files = UploadSet('files', IMAGES+DOCUMENTS)
configure_uploads(app, files)

@app.route('/API-2', methods=['GET', 'POST'])
def upload():
    tasks = Task.query.all()
    if request.method == 'POST' and 'file' in request.files:
        filename = files.save(request.files['file'])
        content = filename
        task = Task(content)
        db.session.add(task)
        db.session.commit()
        f = open('Upload Files.txt','a')           # Opening text file
        f.write('\n'+' API-1* '+filename)          # Saving uploaded file name with extension
        f.close()                                  # Closing the text file
        return redirect(request.url), lastname(names)
    return render_template('upload.html', tasks=tasks)

##########################     THE COUNT FUNCTION       #########################

def lastname(names):
    
    c=0
    for name in names:
        lowercase=name.lower()
        splitname=lowercase.split()
        length=len(splitname)

        if splitname[length-1] == 'siddiqui':
            c=c+1
    return c

if __name__ == '__main__':
    app.run(debug=True)