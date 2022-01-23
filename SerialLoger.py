import time
import serial

from tkinter import *
from tkinter import filedialog



def getSerialPorts():
    from serial.tools import list_ports_windows
    prt=[]
    for port, desc, hwid in sorted(list_ports_windows.comports()):
        prt.append(port)

    return prt

def beginSerialports(prt_list):
    srl_list = []
    for prt in prt_list:
        srl_list.append(serial.Serial(port=prt, baudrate=57600, timeout=2))

    return srl_list

def openFiles(mode, prt_list):
    for prt in prt_list: 
        if mode=='r':
            with open(f"{directory}{prt+'e'}.txt", 'w') as f:
              f.write('\n'+time.ctime()+'\n')

        elif mode=='a':
            with open(f"{directory}{prt+'e'}.txt", 'a') as f:
             f.write('\n'+time.ctime()+'\n')

# Main=======================================================
win = Tk()
win.wm_withdraw()
directory = filedialog.askdirectory()
win.destroy()
if directory!="":
    directory+="/"
print(f"Files will be writen in: {directory}")

prt_list = getSerialPorts()
srl_list = beginSerialports(prt_list)
print(f"Available serial ports: {prt_list}")

openFiles(str(input("Rewrite or apend? r/a")), prt_list)


while srl_list:
    try:
        for srl in srl_list:
            if srl.inWaiting():
                cc = srl.readline()[0:-1].decode('unicode_escape')
                print(time.ctime(), srl.port, cc)
                with open(f"{directory}{srl.port+'e'}.txt", 'a') as f:
                    f.write(cc)
    except:
        prt_list = getSerialPorts()
        srl_list = beginSerialports(prt_list)
