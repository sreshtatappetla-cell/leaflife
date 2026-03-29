from flask import Flask, render_template, request, redirect
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        if 'leaf_image' not in request.files:
            return redirect(request.url)

        file = request.files['leaf_image']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{counter}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                counter += 1

            file.save(filepath)

            # Dummy prediction (replace with model later)
            percent = random.randint(50, 100)

            if percent > 75:
                label = "Fresh"
                shelf = "5-7 days"
            elif percent > 50:
                label = "Moderate"
                shelf = "2-3 days"
            else:
                label = "Spoiled"
                shelf = "Use immediately"

            result = {
                "percentage": percent,
                "label": label,
                "shelf_life": shelf
            }

            return render_template('analyze.html', result=result, filename=filename)

    return render_template('analyze.html', result=None)

@app.route('/storage')
def storage():
    return render_template('storage.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
