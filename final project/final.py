import serial
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
import cv2
import mediapipe as mp
import pyttsx3
import pyfirmata
import controller as cnt

# from PIL import ImageGrab
#https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl    for dlib
#also install spyder


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
engine = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",140)
engine.setProperty("volume",1000)





path = 'F:\DIY ASSIGNMENT\images'
images = []
classNames = []
myList = os.listdir(path)
i=0
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
facerec=0
start= time.time()
close=time.time()
while close-start<10:
    close2=time.time()
    close=close2
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            facerec=1
            if i==0:
                print("face_recognition completed you can enter the room")
                speak("face recognition completed...opening the door for five seconds")
                cnt.door(facerec)
                i=1
            
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
if facerec==0:
    speak("face recognition is not completed...please try again")
cv2.destroyAllWindows()








mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands


tipIds=[4,8,12,16,20]

video=cv2.VideoCapture(0)
j=0
var1=0
var2=0
var3=0
var4=0
var5=0
var6=0
with mp_hand.Hands(min_detection_confidence=0.8,
               min_tracking_confidence=0.8) as hands:
    while facerec!=0:
        if j==0:
            speak("turning on the room lights...")
            speak("you can control the appliances through hand gestures now")
            j=1
            var6=1
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
    
            if total==0:
                var2=0
                var3=0
                var4=0
                var5=0
                var6=0
                cv2.rectangle(image, (20, 300), (400, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "Light Off", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                if var1==0:
                    speak("turning off the room lights")
                    cnt.control(total)
                    var1=1

            elif total==1:
                var1=0
                var3=0
                var4=0
                var5=0
                var6=0
                cv2.rectangle(image, (20, 300), (500, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "fan speed 1", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                if var2==0:
                    speak("turning fan on")
                    cnt.control(total)
                    var2=1

            elif total==2:
                var2=0
                var1=0
                var4=0
                var5=0
                var6=0
                cv2.rectangle(image, (20, 300), (500, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "fan speed 2", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                if var3==0:
                    speak("turning fan off")
                    cnt.control(total)
                    var3=1

            elif total==3:
                var2=0
                var3=0
                var1=0
                var5=0
                var6=0
                cv2.rectangle(image, (20, 300), (500, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "fan speed 3", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                if var4==0:
                    speak("opening door")
                    cnt.control(total)
                    var4=1

            elif total==4:
                var2=0
                var3=0
                var4=0
                var1=0
                var6=0
                cv2.rectangle(image, (20, 300), (400, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "Fan off", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                if var5==0:
                    speak("closing door")
                    cnt.control(total)
                    var5=1

            elif total==5:
                var2=0
                var3=0
                var4=0
                var5=0
                var1=0
                cv2.rectangle(image, (20, 300), (400, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "Light On", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                if var6==0:
                    speak("turning on the room lights")
                    cnt.control(total)
                    var6=1

            #print(total)
            #cnt.control(total)

        cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
        
video.release()
cv2.destroyAllWindows()



