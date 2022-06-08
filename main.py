import cv2
import math

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

cv2.destroyAllWindows()

print(pdict)

def pt_order(curr_pt, pts):
    pt_lst = []
    print()
    while len(pt_lst) < len(pts):
        min_dist = float("inf")
        for pt in pts:
            if pt not in pt_lst:
                dist = abs(curr_pt[0] - pt[0])*110574 + abs((curr_pt[1] - pt[1])*111320*math.cos(pt[1]*math.pi/180))
                if dist < min_dist:
                    min_dist = dist
                    min_pt = pt
        pt_lst.append(min_pt)
        curr_pt = min_pt
        print(min_pt, min_dist/1000, 'km')
    return pt_lst

cur_loc = (0, 0)

print(pt_order(cur_loc, pdict.keys()))

input("Press Enter to continue...")