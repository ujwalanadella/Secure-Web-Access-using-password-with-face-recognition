import cv2
import face_recognition
import getpass
import os
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify

app = Flask(__name__)

# Usernames and their passwords
user_passwords = {
    "sanju": "sanju123",
    "yashu": "yashu123",
    "prasanna": "prasanna123",
    "ujju": "ujju123"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    username = request.form['username']
    capture_images(username)
    return render_template('capture_success.html')

# Function to capture images and store them in a folder
def capture_images(name, num_images=5):
    image_folder = f"/Users/nadellaujwala/Documents/SE PROJECT/{name}"
    os.makedirs(image_folder, exist_ok=True)
    
    video_capture = cv2.VideoCapture(0)
    for i in range(num_images):
        ret, frame = video_capture.read()
        cv2.imwrite(f"{image_folder}/image_{i+1}.jpg", frame)
        cv2.waitKey(1000)  # Pause for 1 second between each capture
    video_capture.release()
    cv2.destroyAllWindows()

@app.route('/recognize')
def recognize_and_verify():
    # Load known face encodings and names
    known_face_encodings = []
    known_face_names = []
    
    # Load known faces and their names here
    known_persons = ["sanju", "yashu", "prasanna", "ujju"]
    for name in known_persons:
        known_person_image = face_recognition.load_image_file(f"/Users/nadellaujwala/Documents/SE PROJECT/{name}.jpg")
        known_person_encoding = face_recognition.face_encodings(known_person_image)[0]
        known_face_encodings.append(known_person_encoding)
        known_face_names.append(name.capitalize())
    
    # Initialize webcam
    video_capture = cv2.VideoCapture(0)

    # Flag to track if a person is recognized
    recognized = False

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not recognized:  
            # Find all face locations in the current frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Check if the face matches any known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # Draw a box around the face and label with the name
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                    recognized = True  
                    break  

            # Display the frame for a short time
            #cv2.imshow("Video", frame)
            cv2.waitKey(500)  

            # Inside recognize_and_verify function, after confirming the name
            name = name.lower()  # Convert name to lowercase
            confirm = input(f"Are you {name.capitalize()}? (yes/no): ")
            if confirm.lower() == "yes":
                 print(f"Hi {name.capitalize()}, please enter your password.")
                 password_input = getpass.getpass("Password: ")

                 if user_passwords.get(name) == password_input:  # Check password using lowercase name
                      print("Password correct, access granted.")
                 else:
                      print("Password incorrect, access denied.")
                      break

                 break

        else:
            cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return 'Face recognition result'
# Main function
def main():
    name = input("Enter your name: ")
    capture_images(name)
    command = input("Do you want to access or enter the website now? (yes/no): ")
    if command.lower() == "yes":
        recognize_and_verify()

if __name__ == "__main__":
    app.run(debug=True)
