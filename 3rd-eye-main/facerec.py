import cv2
import face_recognition
import os
import requests

def find_match(input_image_path, database_folder):
    # Load the input image and create the encoding
    input_img = cv2.imread(input_image_path)
    input_img_rgb = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    input_encoding = face_recognition.face_encodings(input_img_rgb)[0]

    # Traverse the folder containing the database images
    for file_name in os.listdir(database_folder):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):  # Filter image files
            # Load the image from the database
            db_image_path = os.path.join(database_folder, file_name)
            db_img = cv2.imread(db_image_path)
            db_img_rgb = cv2.cvtColor(db_img, cv2.COLOR_BGR2RGB)

            # Create the encoding for the database image
            db_encoding = face_recognition.face_encodings(db_img_rgb)
            if len(db_encoding) > 0:  # Check if encoding is found
                db_encoding = db_encoding[0]

                # Compare the input image encoding with the database image encoding
                result = face_recognition.compare_faces([input_encoding], db_encoding)

                # If a match is found, return the ID
                if result[0]:
                    name = os.path.splitext(file_name)[0]  # Extract the ID
                    print(f"Match found with: {name}")
                    return True, name
    return False, None

# Define the database folder and capture an image
database_folder = "criminal"
input_image = "chitrak.jpg"

# Run face recognition
match_found, matched_image_name = find_match(input_image, database_folder)

if match_found:
    # Send the ID to System 1's Flask server
    payload = {'id': matched_image_name}
    try:
        response = requests.post('http://127.0.0.1:5000/api/receive-id', json=payload)
        print(response.json())
    except Exception as e:
        print(f"Error sending ID to server: {str(e)}")
else:
    print("No match found.")
