import cv2
import numpy as np
import math

def preprocess(orig):
    face_cascade = cv2.CascadeClassifier('face.xml')

    frame = cv2.GaussianBlur(orig, (11, 11), 0)
    faces = face_cascade.detectMultiScale(orig, 1.3, 5)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.inRange(frame, (3, 50, 50), (15, 255, 255))
    frame = cv2.medianBlur(frame, 11)
    frame = cv2.erode(frame, None, iterations=1)
    if faces != ():
        for face in faces:
            (x, y, w, h) = face
            frame[y - 50:y + h, x:x + w] = 0

    _frame = np.zeros(frame.shape)


    contours, hierarchy = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours!=[]:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        _frame[y:y+h, x:x+w] = cv2.medianBlur(frame[y:y+h, x:x+w], 11)
        cv2.rectangle(_frame, (x, y), (x+w, y+h), 255)


        hull = cv2.convexHull(c, returnPoints=False)
        defects = cv2.convexityDefects(c, hull)
        cnt = 0

        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(c[s][0])
            end = tuple(c[e][0])
            far = tuple(c[f][0])
            cv2.line(_frame, start, end, 255, 2)
            # cv2.circle(_frame, far, 5, [0, 0, 255], -1)
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            ci = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = math.acos((b ** 2 + ci ** 2 - a ** 2) / (2 * b * ci))
            if angle <= math.pi / 2:
                cnt += 1
                cv2.circle(_frame, far, 8, 255, -1)

        cnt = 0 if not cnt else cnt+1
        st = "Paper"
        if cnt >=4:
            st = "Paper"
        elif cnt >=2:
            st = "Scissor"
        else:
            st = "Stone"

        cv2.putText(_frame, st, (x,y-50), cv2.FONT_HERSHEY_SIMPLEX, 3,255)
        return _frame