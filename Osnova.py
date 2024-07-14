import cv2
import pickle
import cvzone
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.31.72", # IP-адрес компьютера, где запущен MySQL сервер
  user="ali",
  password="platon1",
  database="my_db"
)

mycursor = mydb.cursor()
mydb.commit()

# Video stream
cap = cv2.VideoCapture('test2.mp4')

j=0
dat=[]
mycursor.execute('Select is_available from parking_spaces')
dat = mycursor.fetchall()
mydb.commit()
with open('PosLand1.pkl', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(framePro,j):

    spaceCounter = 0

    for i, pos in enumerate(posList):

        x1, y1 = pos[0]
        x2, y2 = pos[1]
        # print(i,j)
        frameCrop = framePro[y1:y2, x1:x2]
        count = cv2.countNonZero(frameCrop)

        if count < 1400:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            carr = True
            if dat[j]!=carr:
                sql = "UPDATE parking_spaces SET is_available = %s WHERE id = %s"
                mycursor.execute(sql, (carr, i))
                mydb.commit()
                dat[j]=carr

        else:
            color = (0, 0, 255)
            thickness = 2
            carr = False
            if dat[j] != carr:
                sql = "UPDATE parking_spaces SET is_available = %s WHERE id = %s"
                mycursor.execute(sql, (carr,i))
                mydb.commit()
                dat[j] = carr

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        cvzone.putTextRect(frame, str(i), (x1, y2 - 3), scale=1, thickness=2, offset=0, colorR=color)
        j+=1
    cvzone.putTextRect(frame, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=2, thickness=5, offset=20, colorR=(0, 200, 0))

    return spaceCounter
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frameBlur = cv2.GaussianBlur(frameGray, (3, 3), 1)
    frameThreshold = cv2.adaptiveThreshold(frameBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    frameMedian = cv2.medianBlur(frameThreshold, 5)
    kernal = np.ones((3, 3), np.uint8)
    frameDilate = cv2.dilate(frameMedian, kernal, iterations=1)

    spacecount = checkParkingSpace(frameDilate,j)

    cv2.imshow('Image', frame)
    # cv2.imshow('Tresh', frameThreshold)
    cv2.imshow('Image1', frameDilate)
    cv2.waitKey(10)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()