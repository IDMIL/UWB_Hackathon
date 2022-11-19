


# Standard libraries
from subprocess import Popen, run,PIPE
import time
import sys
import serial
import numpy as np
import pandas as pd

BAUDRATE = "115200"
READ_TIMEOUT_SECS = 5.0

DATA_START = b'<<<'
DATA_END = b'\n'

# Ports
txPort = 'COM9'
rxPort = 'COM8'
dur = 120

# Setup testing parameters
tx_delay = 100 #ms
msg_length = 12 #bytes
board_dist = 0 #cm

# Setup Threads
p1 = Popen(['python', './ReadCOM.py', txPort, BAUDRATE, str(dur)], stdout=PIPE,text=True) 
p2 = Popen(['python', './ReadCOM.py', rxPort, BAUDRATE, str(dur)], stdout=PIPE,text=True)

start_time = time.perf_counter()
cur_time = 0

while ((p2.poll() is None) or (p1.poll() is None)):
    print("Still working...")
    # sleep a while
    # time_passed = time.perf_counter()-start_time
    # if np.mod(time_passed,10) < 0.01:
    #     print("messages received from TX: %s" % p1.stdout.readline()) # print output from ReadCOM.py for rx
    #     print("messages received from RX: %s" % p2.stdout.readline()) # print output from ReadCOM.py for tx
    # txCount = p1.stdout.read(1)
    # rxCount = p2.stdout.read(1)
    # print("messages received from TX: %s" % p1.stdout.read(1)) # print output from ReadCOM.py for rx
    # print("messages received from RX: %s" % p2.stdout.read(1)) # print output from ReadCOM.py for tx
    cur_time = round(time.perf_counter()-start_time,2)
    print("Elapsed Time: " + str(cur_time) +"s")
    time.sleep(1)
    continue

print("Test Done, see files")

# Analyse Reliability
rxdf = pd.read_csv("messagesReceived_RX.csv")
txdf = pd.read_csv("messagesReceived_TX.csv")

# Print Analysis
reliability = (1-abs(len(rxdf)-len(txdf))/len(txdf))*100
print("Precentage of messages received: " + str(reliability) + "%")

# Save results of analysis
reliabilityPD = pd.DataFrame({"Reliability" : [reliability],"Duration" : [dur], "TX Delay" : [tx_delay],"Message Length" : [msg_length]})
fileName = "reliabilityResults/results_dur"+str(dur)+"_txdelay"+str(tx_delay)+"_msglength"+str(msg_length)+"_boardist"+str(board_dist)+".csv"
reliabilityPD.to_csv(fileName, encoding='utf-8', index=False)