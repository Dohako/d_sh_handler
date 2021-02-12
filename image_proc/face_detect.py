import cv2
import winsound

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray,1.2,6)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
        print('face')

    cv2.imshow('rez',img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()