from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Firebase Realtime Database URL
FIREBASE_URL = 'https://dashboard-f40db-default-rtdb.europe-west1.firebasedatabase.app'

# Route to display the buttons
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def original_page():
    return render_template('new.html')

# Route to handle button state changes
@app.route('/update_state', methods=['POST'])
def update_state():
    data = request.json
    company = data['company']       # The name of the selected company
    row = data['row']               # The row of the button
    col = data['col']               # The column of the button
    new_state = data['new_state']   # The new state for the button

    # Create or update the button state in Firebase for the selected company
    firebase_url = f'{FIREBASE_URL}/companies/{company}/row{row}/col{col}.json'
    response = requests.put(firebase_url, json=new_state)

    if response.status_code == 200:
        return jsonify({'status': 'success', 'company': company, 'row': row, 'col': col, 'new_state': new_state})
    else:
        return jsonify({'status': 'failed', 'error': response.text}), 500

# Route to retrieve the button states for a company
@app.route('/get_state/<company>', methods=['GET'])
def get_state(company):
    # Fetch all button states for the company from Firebase
    firebase_url = f'{FIREBASE_URL}/companies/{company}.json'
    response = requests.get(firebase_url)

    if response.status_code == 200:
        data = response.json() or {}
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

# Route to add a new company
@app.route('/add-company', methods=['POST'])
def add_company():
    data = request.json
    company = data['company']

    # Add the company to Firebase if it doesn't exist
    firebase_url = f'{FIREBASE_URL}/companies/{company}.json'
    response = requests.patch(firebase_url, json={})  # Create a new company node if it doesn't exist

    if response.status_code == 200:
        return jsonify({'message': 'Company added successfully!'})
    else:
        return jsonify({'message': 'Failed to add company'}), 500

# Route to get the list of companies
@app.route('/get_companies', methods=['GET'])
def get_companies():
    # Fetch the list of companies from Firebase
    firebase_url = f'{FIREBASE_URL}/companies.json'
    response = requests.get(firebase_url)

    if response.status_code == 200:
        data = response.json() or {}
        companies = list(data.keys())  # Get the list of company names
        return jsonify(companies)
    else:
        return jsonify({'error': 'Failed to fetch companies'}), 500

if __name__ == "__main__":
    app.run(debug=True)
