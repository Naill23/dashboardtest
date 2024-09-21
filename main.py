from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Firebase Realtime Database URL
FIREBASE_URL = 'https://dashboard-f40db-default-rtdb.europe-west1.firebasedatabase.app'

# Route to display the buttons
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle button state changes
@app.route('/update_state', methods=['POST'])
def update_state():
    data = request.json
    user_id = data['user_id']       # The unique ID of the user/client
    row = data['row']               # The row of the button
    col = data['col']               # The column of the button
    new_state = data['new_state']   # The new state for the button

    # Create or update the button state in Firebase
    firebase_url = f'{FIREBASE_URL}/users/{user_id}/row{row}/col{col}.json'
    response = requests.put(firebase_url, json=new_state)

    if response.status_code == 200:
        return jsonify({'status': 'success', 'row': row, 'col': col, 'new_state': new_state})
    else:
        return jsonify({'status': 'failed', 'error': response.text}), 500

# Route to retrieve the button states for a user
@app.route('/get_state/<user_id>', methods=['GET'])
def get_state(user_id):
    # Fetch all button states for the user from Firebase
    firebase_url = f'{FIREBASE_URL}/users/{user_id}.json'
    response = requests.get(firebase_url)

    if response.status_code == 200:
        data = response.json() or {}
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
