import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    _, image = cap.read()
    res, _, _ = detector.detectAndDecode(image)
    if res:
        print(res)
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1)
