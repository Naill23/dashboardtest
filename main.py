from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Firebase Realtime Database URL
FIREBASE_URL = 'https://dashboard-f40db-default-rtdb.europe-west1.firebasedatabase.app'

# Route to display the company selection page
@app.route('/')
def index():
    return render_template('index.html')

# Route to retrieve a list of companies
@app.route('/get_companies', methods=['GET'])
def get_companies():
    firebase_url = f'{FIREBASE_URL}/companies.json'
    response = requests.get(firebase_url)
    
    if response.status_code == 200:
        data = response.json() or {}
        company_names = list(data.keys())  # Get the list of existing companies
        return jsonify(company_names)
    else:
        return jsonify({'error': 'Failed to fetch companies'}), 500

# Route to save button states for a company
@app.route('/update_state', methods=['POST'])
def update_state():
    data = request.json
    company = data['company']     # The company name
    row = data['row']             # The row of the button
    col = data['col']             # The column of the button
    new_state = data['new_state'] # The new state for the button

    # Save button states under the company in Firebase
    firebase_url = f'{FIREBASE_URL}/companies/{company}/row{row}/col{col}.json'
    response = requests.put(firebase_url, json=new_state)

    if response.status_code == 200:
        return jsonify({'status': 'success', 'row': row, 'col': col, 'new_state': new_state})
    else:
        return jsonify({'status': 'failed', 'error': response.text}), 500

# Route to retrieve the button states for a specific company
@app.route('/get_state/<company>', methods=['GET'])
def get_state(company):
    firebase_url = f'{FIREBASE_URL}/companies/{company}.json'
    response = requests.get(firebase_url)

    if response.status_code == 200:
        data = response.json() or {}
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
