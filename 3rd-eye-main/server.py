from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Endpoint to receive ID
@app.route('/api/receive-id', methods=['POST'])
def receive_id():
    data = request.json

    # Validate the input
    if not data or 'id' not in data:
        return jsonify({"status": "failure", "message": "ID not provided"}), 400

    received_id = data['id']
    print(f"Received ID: {received_id}")

    # Forward the ID to System 2
    system2_url = "http://192.168.1.15:5001/api/search-id"  # Replace with System 2's actual IP and port
    try:
        # Send the POST request to System 2
        response = requests.post(system2_url, json={"id": received_id})
        
        # Check if the request was successful
        if response.status_code == 200:
            system2_response = response.json()
            print(f"Response from System 2: {system2_response}")
            return jsonify(system2_response)  # Return System 2's response back to the client
        else:
            return jsonify({
                "status": "failure",
                "message": f"Failed to reach System 2, Status Code: {response.status_code}"
            }), response.status_code

    except Exception as e:
        print(f"Error forwarding ID to System 2: {str(e)}")
        return jsonify({"status": "failure", "message": f"Error forwarding ID: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Make server accessible on the network
