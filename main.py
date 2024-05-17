import cmake
import face_recognition as fr
import cv2
import numpy as np
import csv
from datetime import date, datetime

video_capture = cv2.VideoCapture(0)

# load known faces
zarana_image = fr.load_image_file("face/zarana.jpg")
zarana_encoding = fr.face_encodings(zarana_image)[0]

hinal_image = fr.load_image_file("face/hinal.jpeg")
hinal_encoding = fr.face_encodings(hinal_image)[0]

known_face_encodings = [zarana_encoding,hinal_encoding]
known_face_names = ["zarana","hinal"]

# list of expected students
students = known_face_names.copy()

face_locations = []
face_encodings = []

# get the current tine and date
now = datetime.now()
current_date = now.strftime("%y-%m-%d")

f = open(f"{current_date}.csv","w+",newline="")
lnwrite = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognize faces
    face_locations = fr.face_locations(rgb_small_frame)
    face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        mathes = fr.compare_faces(known_face_encodings,face_encoding)
        face_distance = fr.face_distance(known_face_encodings,face_encoding)
        best_mathce_index = np.argmin(face_distance)

        if(mathes[best_mathce_index]):
            name = known_face_names[best_mathce_index]

        # Add the text if person is present
        if name in known_face_names:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10,100)
            fontScale = 1.5
            fontcolor = (155,0,0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Present", bottomLeftCornerOfText,font,fontScale,fontcolor,thickness,lineType)

            if name in students:
                students.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwrite.writerow([name, current_time])

    cv2.imshow("Attendence",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print("Your Attendene Counted")
video_capture.release()
cv2.destroyAllWindows()
f.close()