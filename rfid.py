import time
import serial
import requests
import json

serial = serial.Serial("/dev/tty.usbserial-A101NC8U", 9600)
url= "http://127.0.0.1/OnetoOne/api/toggle.php"
key = "1B7D5575BAD62F6BA3C6D1163A786"

helpers = []
send_data = {
    "id": 0
}
send = {
    "data": "",
    "key" : key
}

f = open("helpers.txt", "r+")
for line in f:
    line = line.replace("\n", "")
    data = line.split(", ")
    helpers.append([data[0], data[1]])
f.close()
while True:
    if serial.inWaiting() > 0:
        read_result = serial.read(12)
        rfid = format(read_result.decode(encoding="utf-8"))
        if len(rfid) == 12:
            rfid = rfid[1:11]
            print("Read card " + rfid)
            for student in helpers:
                if(rfid == student[0]):
                    print "You are " + student[1]
                    send_data["id"] = student[1]
                    send["data"] = json.dumps(send_data)
                    print requests.post(url, data=send).text
        else:
            print("Misread card")
        print("Please wait for 1 second...");
        time.sleep(1)
        serial.flushInput() # ignore errors, no data
