#main.py

from dronekit import *
import time
from scan import scan_products
from sys import exit


#connect to vehicle
vehicle=connect('127.0.0.1:14551',baud=921600,wait_ready=True)

while True:
    pdict = scan_products()
    if not pdict:
        print("Try again!")
    else:
        break

cur_cord = (vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon)
print("Current coordinates of the drone are:",cur_cord)

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

way_pt_lst = pt_order(cur_cord, pdict.keys())

print(way_pt_lst)

#takeoff function
def toff(height):
    #check if drone is ready
    while not vehicle.is_armable:
        print("Waiting for drone")
        time.sleep(1)
    #change mode and arm
    print('arming')
    vehicle.mode=VehicleMode('GUIDED')
    vehicle.armed=True
    #check if drone is armed
    while not vehicle.armed:
        print("Waiting for arm")
        time.sleep(1)
    #takeoff
    print('take-off')
    vehicle.simple_takeoff(height)
    #report values back every 1s and finally break out
    while True:
        print('Reached',vehicle.location.global_relative_frame.alt)
        if(vehicle.location.global_relative_frame.alt>=height*0.95):
            print('reached target altitude')
            break
        time.sleep(1)
# toff(10)#Ten meters of height
# #hover in 10s
# time.sleep(10)# as 10 seconds we put 10
# #landing
# print("Land")
# vehicle.mode=VehicleMode('RTL')
# time.sleep(20)
# #close vehicle
# vehicle.close()
