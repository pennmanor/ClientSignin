import time
import serial
import requests
import json

device= ""
url= ""
key = ""

serial = serial.Serial(device, 9600)
helpers = []
send_data = {
    "id": 0
}
send = {
    "data": "",
    "key" : key
}
print "Reading files"
f = open("helpers.txt", "r+")
for line in f:
    line = line.replace("\n", "")
    data = line.split(", ")
    helpers.append([data[0], data[1]])
f.close()
print "Done. Ready to scan."
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
    else:
        time.sleep(0.1)

