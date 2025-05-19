from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

# import libraries on read_file.py
from read_file import load_data, filter_data

app = Flask(__name__)
UPLOAD_FOLDER = './data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r"/data": {"origins": "*"}})
# Set the maximum file size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Set the allowed file types

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Endpoint to upload xlsx file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200
    else:
        return jsonify({'error': 'Invalid file type. Only .xlsx files are allowed'}), 400

# Endpoint to consume the info in JSON
@app.route('/data', methods=['GET'])
def get_data():
    # Get the semester from the query parameters
    semestre = request.args.get('semestre')
    if not semestre:
        return jsonify({'error': 'Semester parameter is required'}), 400
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    if not filename:
        filename = 'R3DET 8.0.xlsx'
    # Construct the file path
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Check if the file exists
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    # Load the data
    try:
        data = load_data(filepath, 'TG')
    except Exception as e:
        return jsonify({'error': f'Failed to load file: {str(e)}'}), 500
    # Filter the data
    try:
        filtered_data = filter_data(data, semestre)
    except Exception as e:
        return jsonify({'error': f'Failed to filter data: {str(e)}'}), 500
    # Convert the filtered data to JSON
    try:
        # filtered_data_json = filtered_data.to_dict(orient='records')
        # json with 2 plots
        #filtered_data_json = {
        #    'egresados': filtered_data['Eg'].tolist(),
        #    'titulados': filtered_data['STit'].tolist(),
        #    'cambios_carrera': filtered_data['ECC'].tolist(),
        #    'cambios_6ta_oportunidad': filtered_data['ECC6'].tolist(),
        #    'periodo': filtered_data['Per'].tolist()
        #}

        # filter data like array
        filtered_data_json = [
            {
                'egresados': row['Eg'],
                'titulados': row['STit'],
                'cambios_carrera': row['ECC'],
                'cambios_6ta_oportunidad': row['ECC6'],
                'periodo': row['Per']
            }
            for index, row in filtered_data.iterrows()
        ]
    except Exception as e:
        return jsonify({'error': f'Failed to convert data to JSON: {str(e)}'}), 500
    # Return the filtered data as JSON
    return jsonify(filtered_data_json), 200



if __name__ == '__main__':
    app.run(debug=True)
