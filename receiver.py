import cv2
import bcrypt

def authenticate(hashed):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    wrong_pass = []

    while len(wrong_pass) < 3:
        _, image = cap.read()
        res, _, _ = detector.detectAndDecode(image)
        if res:
            if bcrypt.checkpw(res.encode(), hashed):
                print("Authenticated")
                return 1
            elif res not in wrong_pass:
                wrong_pass.append(res)
                print("Wrong Code. Try again.")
            else:
                print("Wrong Code. Try again.")
        cv2.imshow("Frame", image)
        key = cv2.waitKey(100)
    print("Authentication failed. Too many wrong attempts.")
    return 0

if "__main__" == __name__:
    print(authenticate(bcrypt.hashpw("&NcEZnjn=9".encode('utf-8'), bcrypt.gensalt())))