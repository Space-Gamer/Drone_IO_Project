import pyqrcode
import string
import bcrypt
import random

lat = float(input("Latitude: "))
lon = float(input("Longitude: "))

passlen = 10
passwd = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(passlen))
hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

pasqr = pyqrcode.create(passwd)
prodqr = pyqrcode.create(str((lat, lon))+' '+hashed.decode('utf-8'))
pasqr.show()
prodqr.show()
if input("Do you want to save the QR codes? (y/n): ") == 'y':
    pasqr.svg('passwd.svg', scale=8)
    prodqr.svg('product.svg', scale=8)