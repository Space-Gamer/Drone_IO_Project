import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

nop = int(input("Enter number of products to be scanned: "))
pdict = {}

while (len(pdict) < nop):
    _, image = cap.read()
    res, _, _ = detector.detectAndDecode(image)
    if res:
        try:
            lst = res.split()
            if type(eval(lst[0])) == tuple and tuple(eval(lst[0])) not in pdict.keys():
                pdict[tuple(eval(lst[0]))] = lst[1]
                print("Product scanned: ", lst[0])
        except IndexError:
            print("Invalid QR code")
        except Exception as e:
            print(e)
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1)

print(pdict)
