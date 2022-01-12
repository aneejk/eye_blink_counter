import cv2
from mesh import GetFaceMeshCord, points_Distance
import argparse
import sys
opt = argparse.ArgumentParser()
opt.add_argument('-s',default=0)
opt.add_argument('-d',default=False,action='store_true')
args = opt.parse_args()
print("Input stream Name or device_id", args.s)
cap = cv2.VideoCapture(args.s)
ratioList = []                    
blinkCounter = 0                                   
counter = 0
color = (255, 0, 255)
 
while True:
    key=cv2.waitKey(1)
    if key%256 == 27:
        cv2.destroyAllWindows()
        sys.exit()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
 
    ret, frame = cap.read()
    if ret:
        faces,img = GetFaceMeshCord(frame, draw=args.d)
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
            color = (255,255,255)
            if ratioAvg < 25 and counter == 0:
                blinkCounter += 1
                counter = 1
            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0
            x,y,w,h = 0,0,175,50

            # Draw black background rectangle
            cv2.rectangle(img, (20, 20), (20 + w, 20 + h), (0,0,0), -1)
    
            img =cv2.putText(img, f'Blink Count: {blinkCounter}', (20, 50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.9,color,2,cv2.FILLED)
        #cv2.imshow("Input", frame)
        #cv2.waitKey(25)
        cv2.imshow("Output", img)
        cv2.waitKey(25)
        
            