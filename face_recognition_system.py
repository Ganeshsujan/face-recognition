# Install required libraries
%pip install opencv-python
%pip install face_recognition
%pip install numpy

import cv2
import face_recognition
import numpy as np

class FaceRecognitionSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.camera = cv2.VideoCapture(0)
        
    def add_person(self, name):
        print(f"Adding {name} to the system...")
        print("Please look at the camera...")
        
        while True:
            ret, frame = self.camera.read()
            cv2.imshow('Adding New Face', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('s'):  # Press 's' to save
                face_locations = face_recognition.face_locations(frame)
                if len(face_locations) == 1:
                    face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(name)
                    print(f"Successfully added {name}!")
                    cv2.destroyAllWindows()
                    break
                else:
                    print("Please ensure exactly one face is visible")
            
            elif cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                cv2.destroyAllWindows()
                break
    
    def start_recognition(self):
        print("Starting face recognition. Press 'q' to quit.")
        
        while True:
            ret, frame = self.camera.read()
            
            # Find all faces in the current frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            # Loop through each face in this frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                
                # Draw rectangle and name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display the resulting frame
            cv2.imshow('Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()
    
    def __del__(self):
        self.camera.release()

# Create and use the system
face_system = FaceRecognitionSystem()

# Add some people (you can add multiple people)
face_system.add_person("User")  # Press 's' to save the face, 'q' to quit

# Start recognition
face_system.start_recognition()  # Press 'q' to quit