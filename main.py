import os
import face_recognition as fr
import cv2
import numpy as np
import csv
from datetime import datetime, time
import pyttsx3  # Text-to-speech library
import time as tm

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize video capture for the webcamara
video_capture = cv2.VideoCapture(0)

# Check if the webcamara opened or not
if not video_capture.isOpened():
    print("Error: Unable to access the webcam.")
    engine.say("Error: Unable to access the webcam.")
    engine.runAndWait()
    exit()  # Exit the program if webcamara not open 

print("Webcam opened successfully")
engine.say("Webcam opened successfully")
engine.runAndWait()

# Load known faces  from the 'face' folder
face_folder = "face"
known_face_encodings = []
known_face_names = []

for filename in os.listdir(face_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # image files with this extensions
        image_path = os.path.join(face_folder, filename)
        image = fr.load_image_file(image_path)
        encoding = fr.face_encodings(image)
        if len(encoding) > 0:  
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])  # Use the filename as the studentname

if not known_face_encodings:
    print("No known faces loaded. Exiting.")
    engine.say("No known faces loaded. Exiting.")
    engine.runAndWait()
    video_capture.release()
    cv2.destroyAllWindows()
    exit()

# List of expected students 
students = {name: "Absent" for name in known_face_names}

# Date for attendance register
current_date = datetime.now().strftime("%Y-%m-%d")

# Open CSV file in append mode to record attendance
with open(f"attendance_{current_date}.csv", "a+", newline="") as f:
    lnwrite = csv.writer(f)
    lnwrite.writerow(["Name", "Date", "Time", "Status"])

    while True:
        # Capture video frame-by-frame
        ret, frame = video_capture.read()   # 'ret' is a boolean value indicating whether a frame was successfully read from the video capture
        
        if not ret:
            print("Error: Failed to capture frame.")
            engine.say("Error: Failed to capture frame.")
            engine.runAndWait()
            break  # Exit the loop if no frame is captured

        # Display the webcamara for the user
        cv2.imshow("Attendance System", frame)

        # Process the frame for face recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Recognize faces
        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

        recognized = False  # Flag to track if a face is recognized

        for face_encoding in face_encodings:
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            face_distance = fr.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                recognized = True  # flag = true if face is recognized
                name = known_face_names[best_match_index]

                # Add the text if the person is present
                if students[name] == "Absent":  
                    current_time = datetime.now().strftime("%H:%M:%S")
                    students[name] = "Present"
                    lnwrite.writerow([name, current_date, current_time, "Present"])

                    # Attendance has been taken
                    engine.say(f"{name}, your attendance has been marked.")
                    engine.runAndWait()

                    # Write on the screen
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, f"{name} Present", (50, 50), font, 1, (255, 0, 0), 2)

        # If no face was recognized
        if not recognized and face_encodings:
            engine.say("Face not recognized. Please register yourself.")
            engine.runAndWait()
            print("Face not recognized.")

        # Display the updated webcamara  with recognition results
        cv2.imshow("Attendance System", frame)

        # Allow the user to manually exit the loop by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Check if it's 11:59 PM and mark absentees
        current_time = datetime.now().time()
        end_of_day = time(21, 35)  # 11:59 PM

        if current_time >= end_of_day:
            for student, status in students.items():
                if status == "Absent":
                    print(f"{student} is absent.")
                    lnwrite.writerow([student, current_date, "Absent"])
                    engine.say(f"{student} is absent.")
                    engine.runAndWait()
            break  # Break the loop at 11:59 PM



# Release the webcamara and close windows if not already done
video_capture.release()
cv2.destroyAllWindows()
