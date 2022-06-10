#main.py

from dronekit import *
import time
from scan import scan_products
from receiver import authenticate
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
    print('Take-Off')
    vehicle.simple_takeoff(height)
    #report values back every 1s and finally break out
    while True:
        print('Reached',vehicle.location.global_relative_frame.alt)
        if(vehicle.location.global_relative_frame.alt>=height*0.95):
            print('Reached target altitude.')
            return 1
        time.sleep(1)
    else:
        return 0

def get_dist_metre(a, b):
    return (((a.lat-b.lat)*2+(a.lon-b.lon)2)*0.5)*1.113195e5
    
    
if toff(15):
    for i in range(len(way_pt_lst)):
        vehicle.simple_goto(LocationGlobalRelative(way_pt_lst[i][0],way_pt_lst[i][1],15))
        target_dist = get_dist_metre(LocationGlobalRelative(way_pt_lst[i][0],way_pt_lst[i][1],15),vehicle.location.global_relative_frame)
        while vehicle.mode.name == "GUIDED":
            rem_dist = get_dist_metre(vehicle.location.global_relative_frame,LocationGlobalRelative(way_pt_lst[i][0],way_pt_lst[i][1],15))
            print(f"Distance to target {i+1}: {round(rem_dist,2)}m")
            if (rem_dist<=target_dist*0.01):
                print("Reached target",i+1)
                break
            time.sleep(2.5)
        print("Landing...")
        vehicle.mode = VehicleMode("LAND")
        time.sleep(20)
        try:
            if authenticate(pdict[(way_pt_lst[i][0],way_pt_lst[i][1])].encode()):
                print(f"Package {i+1} delivered")
            else:
                print(f"Package {i+1} was not delivered due to authentication failure.")
            time.sleep(10)
        except Exception as e:
            print(e)
        vehicle.mode = VehicleMode("GUIDED")
        while not(toff(15)):
            print("Trying to lift")
            time.sleep(10)

print("Returning to base")
vehicle.simple_goto(LocationGlobalRelative(cur_cord[0],cur_cord[1],15))
target_dist = get_dist_metre(LocationGlobalRelative(cur_cord[0],cur_cord[1],15),vehicle.location.global_relative_frame)
while vehicle.mode.name == "GUIDED":
            rem_dist = get_dist_metre(vehicle.location.global_relative_frame,LocationGlobalRelative(cur_cord[0],cur_cord[1],15))
            print(f"Distance to inital point is {round(rem_dist,2)}m")
            if (rem_dist<=target_dist*0.01):
                print("Reached initial point")
                break
            time.sleep(2.5)

print("Landing..")
vehicle.mode=VehicleMode('LAND')
time.sleep(20)
#close vehicle
vehicle.close()
print("Mission complete!")
