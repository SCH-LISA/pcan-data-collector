from __future__ import print_function
from PCANBasic import *
import random
import time
import os.path
import datetime
import sys



cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

PCAN_CHANNELs = [PCAN_USBBUS1, PCAN_USBBUS2, PCAN_USBBUS3, PCAN_USBBUS4, PCAN_USBBUS5, PCAN_USBBUS6]

if __name__ == "__main__":
    
    dataset_type = "Normal_CH1"
    x = datetime.datetime.now()
    x = "Dataset\\KIA " + dataset_type + " Dataset " + str(x).split()[0] + "-"
    ind = 0

    while os.path.isfile( x + str(ind) + ".txt"):
        ind += 1
        print("Yes")

    print("No")
    x = x + str(ind) + ".txt"
    f = open(x, "a")

    # all_data = "No\tID\tTYPE\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
    all_data = ""
    for col in cols:
        all_data += col + "\t"

    print(all_data)
    f.write(all_data + "\n")


    CAN = PCANBasic()                            #CANi    
    CAN_BUS = PCAN_CHANNELs[0]
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt

    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    print("Succesfully Connected")
    counter = 0
    ind = 1
    IsFirst = True
    while True: 
        # print("PCAN-USB Pro FD (Ch-1) was initialized")
        mess = CAN.Read(CAN_BUS)    
        if mess[0] != PCAN_ERROR_QRCVEMPTY:
            all_data = str(ind) + ')' + "\t"

            if IsFirst:
                offset = 0
                start_time = mess[2].micros + 1000 * mess[2].millis + 0x100000000 * 1000 * mess[2].millis_overflow
                start_time = start_time / 1000
                IsFirst = False
            else:
                current_time = mess[2].micros + 1000 * mess[2].millis + 0x100000000 * 1000 * mess[2].millis_overflow
                current_time = current_time / 1000
                offset = (current_time - start_time)
            
            all_data += "{:.3f}".format(offset) + "\t"
            id_hex = hex(mess[1].ID)[2:]
            for _ in range(4 - len(id_hex)):
                id_hex = '0' + id_hex.upper()
            
            all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 
            
            for j in range(mess[1].LEN):
                data_hex = hex(mess[1].DATA[j])[2:]
                for _ in range(2 - len(data_hex)):
                    data_hex = '0' + data_hex.upper()

                all_data += "\t" + data_hex.upper()
            for _ in range(mess[1].LEN, 8):
                all_data += "\t" + "-1"
                
            all_data += "\n"
            ind += 1
            print(all_data)
            f.write(all_data)

    # All initialized channels are released
    CAN.Uninitialize(PCAN_NONEBUS)
