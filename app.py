import os
from flask import Flask, render_template, request, redirect, flash, send_from_directory
import pandas as pd
from ml_script import process_csv_and_generate_graph

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Clear the upload and output folders if they exist
def clear_folders():
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error deleting file {file_path}: {e}')

clear_folders()

# Create the upload and output folders if they don't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

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

        # Process the CSV and generate graphs
        try:
            plot_filenames, r_values = process_csv_and_generate_graph(filepath, OUTPUT_FOLDER)
            flash('File uploaded and processed successfully')
            return render_template('results.html', plot_filenames=plot_filenames, r_values=r_values)
        except Exception as e:
            flash(f'Error processing file: {e}')
            return redirect('/')
    else:
        flash('Invalid file format. Please upload a CSV file.')
        return redirect('/')

@app.route('/output/<path:filename>')
def output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
