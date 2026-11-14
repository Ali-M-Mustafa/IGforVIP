#Import Necessary Libraries
import os
import cv2
import picamera
import numpy as np

#Import Code Files
import face_recognition
from play import play
from Vibration import vibrate

#commented code lines should be uncommented when running this file separately 

# camera = picamera.PiCamera()
# camera.resolution = (640,480)
# image = np.empty((480,640, 3), dtype=np.uint8)

people_DIR            = 'people'             #path for reference faces

# Initialize some variables
people_face_encodings = []
names                 = []
face_locations        = []
face_encodings        = []

# Load a sample picture and learn how to recognize it.
for person in os.listdir(people_DIR):
    person_image = face_recognition.load_image_file(f'{people_DIR}/{person}')
    person_face_encoding = face_recognition.face_encodings(person_image)[0]
    if len(person_face_encoding) > 0:
        people_face_encodings.append(person_face_encoding)
    names.append(person)


def look_for_face_in (image) :
    
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    vibrate(50)
    
    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        results = face_recognition.compare_faces(people_face_encodings, face_encoding)
        #defining names in the resluts
        name = None
        if True in results:
            name = names[results.index(True)]   
        return name 

# image = np.empty((480,640, 3), dtype=np.uint8)
# image_center = tuple(np.array(image.shape[1::-1])/2)
# rot_mat = cv2.getRotationMatrix2D(image_center, -90, 1)

face = None
faces = []
#play the names of recognized faces without repetition 
def Run (image) :
    face = look_for_face_in (image)
    if face not in  faces and face is not None :
        play('{}'.format(face))
        print (face)
        faces.append(face)
        if len(faces) > 2 : faces.pop(0)
        
#     cv2.imshow("face recognition",image)
#     cv2.waitKey(1)
# cv2.destroyAllWindows()
# while True :
#     camera.capture(image, format="rgb")
#     image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)     
#     Run (image)
#     if cv2.waitKey(1)== 27 :
#         break
#     
# cv2.destroyAllWindows()
