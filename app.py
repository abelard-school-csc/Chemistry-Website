import os
from flask import Flask, render_template, request, redirect, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Process the CSV (optional)
        df = pd.read_csv(filepath)
        # You can now do something with the CSV data here (e.g., show it to the user)
        flash('File uploaded and processed successfully')
        return redirect('/')
    else:
        flash('Invalid file format. Please upload a CSV file.')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
