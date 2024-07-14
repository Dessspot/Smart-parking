import cv2
import pickle

# width, height = 80, 100
rectangles = []

try:
    with open('PosLand1.pkl', 'rb') as f:
        rectangles = pickle.load(f)
except:
    rectangles = []

def saveRectangles():
    with open('PosLand1.pkl', 'wb') as f:
        pickle.dump(rectangles, f)

def drawRectangles(img):
    for rectangle in rectangles:
        startPoint, endPoint = rectangle
        cv2.rectangle(img, startPoint, endPoint, (0, 255, 0), 2)

def deleteRectangle(x, y):
    for i, rectangle in enumerate(rectangles):
        startPoint, endPoint = rectangle
        if startPoint[0] < x < endPoint[0] and startPoint[1] < y < endPoint[1]:
            rectangles.pop(i)
            saveRectangles()
            break

def mouseClick(events, x, y, flags, params):
    global startPoint, endPoint, isDragging, rectangles

    if events == cv2.EVENT_LBUTTONDOWN:
        startPoint = (x, y)
        endPoint = (x, y)
        isDragging = True
    elif events == cv2.EVENT_MOUSEMOVE:
        if isDragging:
            endPoint = (x, y)
    elif events == cv2.EVENT_LBUTTONUP:
        isDragging = False
        if startPoint != endPoint:
            rectangles.append((startPoint, endPoint))
            saveRectangles()

    elif events == cv2.EVENT_RBUTTONDOWN:
        deleteRectangle(x, y)

    imgCopy = img.copy()
    drawRectangles(imgCopy)
    cv2.imshow('Image', imgCopy)

img = cv2.imread('2.png')
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouseClick)

while True:
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(rectangles)
cv2.destroyAllWindows()
