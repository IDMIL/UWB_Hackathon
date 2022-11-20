import pandas as pd
import numpy as np
import glob
import os

# Analyse the reliability data
parentFolder = "formalResults"
#parentFolder = "occlusionResults"
#parentFolder = "occlusionResults2"

# Create a bunch of empty lists
conditionList = []
reliabilityList = []
distanceList = []
durationList = []
txdelayList = []
msglengthList = []
msgsentList = []
msgrecList = []

# Read each file and save the data
for files in glob.glob(parentFolder+"/*.csv"):
    # Open the file
    temp = pd.read_csv(files)
    
    # Read all the saved data
    reliabilityList.append(temp.Reliability[0])
    durationList.append(temp.Duration[0])
    txdelayList.append(1/(temp['TX Delay'][0]/1000))
    msglengthList.append(temp["Message Length"][0])
    if "Msg received" in temp.columns: # some tests did not save messages received and sent
        msgrecList.append(temp["Msg received"][0])
    else:  
        msgrecList.append('N/A')
    if "Msg Sent" in temp.columns:
        msgsentList.append(temp["Msg Sent"][0])
    else:
        msgsentList.append('N/A')
        
    # Get the distance from file name
    idx = files.find("boardist")
    stop_idx = files.find("_",idx)
    if stop_idx == -1:
        stop_idx = files.find(".") # if board distance specified at the end of the filename
    start_idx = idx+len("boardist")
    tmp_dist = int(files[start_idx:stop_idx])
    distanceList.append(tmp_dist)
    
    # Get condition from file name
    idx = files.find("occl")
    if idx == -1:
        conditionList.append("Open")
    else:
        conditionList.append("Occlusion")

# Create empty dataframe
reliabilityData = pd.DataFrame()

# Add data to pandas dataframe
reliabilityData['Test Condition'] = conditionList
reliabilityData['Test Duration (s)'] = durationList
reliabilityData['Distance (cm)'] = distanceList
reliabilityData['Transmission Rate (Hz)'] = txdelayList
reliabilityData['Message Length (bytes)'] = msglengthList
reliabilityData['Messages Sent'] = msgsentList
reliabilityData['Messages Received'] = msgrecList
reliabilityData['Packet Loss (%)'] = reliabilityList
    
# Checke filename doesn't exist, if it does delete the file
fileName = parentFolder+"_combinedData.csv"
if os.path.exists(fileName):
    os.remove(fileName)
    
# Save the data
reliabilityData.to_csv(fileName,encoding='utf-8')
print("Done saving")