from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database
database = {
    "1": {"Name": "Chitrak Aseri", "Age": 21, "Crime": "Murder", "Location": "Jaipur"},
    "2": {"Name": "Mridul Chamoli", "Age": 30, "Crime": "Fraud", "Location": "Dehradun"}
}

@app.route('/api/search-id', methods=['POST'])
def search_id():
    data = request.json

    # Validate the input
    if not data or 'id' not in data:
        return "", 204  # Return empty response with 204 (No Content) status

    search_id = data['id']
    print(f"Received ID: {search_id}")

    # Perform database lookup or processing
    if search_id in database:
        metadata = database[search_id]
        print(f"Data: {metadata}")
    else:
        print(f"ID {search_id} not found in the database.")

    # No response to System 1
    return "", 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
