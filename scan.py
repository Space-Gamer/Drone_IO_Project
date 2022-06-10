#scan.py

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

def scan_products():
    # initialize mediapipe
    detector = cv2.QRCodeDetector()
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
    mpDraw = mp.solutions.drawing_utils

    pdict = {}


    # Load the gesture recognizer model
    model = load_model('mp_hand_gesture')

    # Load class names
    f = open('gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()

    thumbs_up = 0
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read each frame from the webcam
        _, frame = cap.read()

        # Detect QR codes
        _, image = cap.read()
        res, _, _ = detector.detectAndDecode(image)
        if res:
            try:
                lst = res.split(':')
                if type(eval(lst[0])) == tuple and tuple(eval(lst[0])) not in pdict.keys():
                    pdict[tuple(eval(lst[0]))] = lst[1]
                    print("Product scanned: ", lst[0])
            except IndexError:
                print("Invalid QR code")
            except Exception as e:
                print(e)


        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        # print(result)

        className = ''

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]
                print(className)
                if className == 'thumbs up':
                    thumbs_up += 1
                    if thumbs_up >= 5:
                        print("Scanned")
                        cv2.destroyAllWindows()
                        cap.release()
                        return pdict


        # show the prediction on the frame
        # cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
        #                1, (0,0,255), 2, cv2.LINE_AA)

        # Show the final output
        cv2.imshow("Output", frame)

        if cv2.waitKey(1) == ord('q'):
            # release the webcam and destroy all active windows
            cv2.destroyAllWindows()
            cap.release()
            return []

if "__main__" == __name__:
    prddict = scan_products()
    if not prddict:
        print("No products scanned")
    else:
        print("Products scanned: ", prddict)
