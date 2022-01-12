import cv2
from mesh import GetFaceMeshCord, points_Distance
import argparse
opt = argparse.ArgumentParser()
opt.add_argument('-s',default=0)
args = opt.parse_args()
print(args.s)
cap = cv2.VideoCapture(args.s)
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243, 252,255,385,249,341,362]
ratioList = []                    
blinkCounter = 0                                   
counter = 0
color = (255, 0, 255)
 
while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
 
    ret, img = cap.read()
    if ret:
        faces,img = GetFaceMeshCord(img, draw=False)
        if len(faces) != 0:
            face = faces[0]
    
            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            rightUp = face[385]
            rightDown = face[252]
            rightRight = face[362]
            rightLeft =face[249]
            lenghtlVer= points_Distance(leftUp, leftDown)
            lenghtlHor= points_Distance(leftLeft, leftRight)
            lenghtrHor= points_Distance(rightLeft, rightRight)
            lenghtrVer= points_Distance(rightUp, rightDown)

            img = cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
            img =cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)
            img = cv2.line(img, rightUp, rightDown, (0, 200, 0), 3)
            img =cv2.line(img, rightLeft, rightRight, (0, 200, 0), 3)
    
            ratio = int((lenghtlVer / lenghtlHor) * 100)
            ratioList.append(ratio)
            if len(ratioList) > 3:
                ratioList.pop(0)
            ratioAvg = sum(ratioList) / len(ratioList)
    
            if ratioAvg < 25 and counter == 0:
                blinkCounter += 1
                color = (0,200,0)
                counter = 1
            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0
                    color = (255,0, 255)
    
            img =cv2.putText(img, f'Blink Count: {blinkCounter}', (50, 100),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2,cv2.FILLED)
    
        cv2.imshow("Image", img)
        cv2.waitKey(25)