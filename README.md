# Face Time Keeper

A "Face Time Keeper" is a system is one of example of Computer vision and face recognition technology. It capture real-time video using a webcam, detects faces from the video, and compares them with pre-stored face data to recognize individuals. Once an individual is recognized, their attendance is automatically recorded in a CSV file. The system also supports text-to-speech feedback to notify users when their attendance has been successfully marked.
## ✨ Features ✨

- Real-Time Face Recognition:📽️
Uses a webcam to capture video and detect faces in real-time.
Compares detected faces with pre-stored face data for recognition.

- Dynamic Face Loading:📂
Loads face data dynamically from the 'face' folder where users' images are stored.
Each image corresponds to a user, and their name is derived from the filename.

- Attendance Recording:📝
Automatically records the attendance of recognized individuals, including their name, date, and time in a CSV file.
Attendance is marked only once per day for each person to avoid duplicates.

- Text-to-Speech Feedback:🔊
Provides audible feedback when attendance is successfully marked or if a face is not recognized.

- Unrecognized Faces Handling:🚫
If an unknown face is detected, it announces that the person is not recognized and prompts them to register.

- Absence Handling:❌
By 12:00 AM, if any faces from the ‘face’ folder are not recognized, they are marked as absent automatically.


