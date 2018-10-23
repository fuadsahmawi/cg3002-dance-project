import pandas as pd

chicken = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\chicken.csv") #label = 3

number7 = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\number7.csv") #label = 2

sidestep = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\sidestep.csv") #Label = 4

wipers = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\wipers.csv") #Label = 1

turnclap = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\turnclap.csv") #Label = 5

neutral = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\neutral.csv") #Label = 0

i=0
features = []
labels = []
feature = []
numOfData = 40
overlapNum = 4 #0.1*numOfData = 90% overlap
numRowsOfChicken = chicken.shape[0] #number of rows in the dataframe

for line in chicken.iterrows():
    
    sumAccX1 = 0
    sumAccY1 = 0
    sumAccZ1 = 0
    sumAccX2 = 0
    sumAccY2 = 0
    sumAccZ2 = 0
    sumGyrX1 = 0
    sumGyrY1 = 0
    sumGyrZ1 = 0
    sumGyrX2 = 0
    sumGyrY2 = 0
    sumGyrZ2 = 0

    
    for index in range(numOfData):
        sumAccX1 = sumAccX1 + chicken.accx1[i+index]
        sumAccY1 = sumAccY1 + chicken.accy1[i+index]
        sumAccZ1 = sumAccZ1 + chicken.accz1[i+index]
        sumAccX2 = sumAccX2 + chicken.accx2[i+index]
        sumAccY2 = sumAccY2 + chicken.accy2[i+index]
        sumAccZ2 = sumAccZ2 + chicken.accz2[i+index]
        sumGyrX1 = sumGyrX1 + chicken.gyrx1[i+index]
        sumGyrY1 = sumGyrY1 + chicken.gyry1[i+index]
        sumGyrZ1 = sumGyrZ1 + chicken.gyrz1[i+index]
        sumGyrX2 = sumGyrX2 + chicken.gyrx2[i+index]
        sumGyrY2 = sumGyrY2 + chicken.gyry2[i+index]
        sumGyrZ2 = sumGyrZ2 + chicken.gyrz2[i+index]
    
    meanAccX1 = sumAccX1/numOfData
    meanAccY1 = sumAccY1/numOfData
    meanAccZ1 = sumAccZ1/numOfData
    meanAccX2 = sumAccX2/numOfData
    meanAccY2 = sumAccY2/numOfData
    meanAccZ2 = sumAccZ2/numOfData
    meanGyrX1 = sumGyrX1/numOfData
    meanGyrY1 = sumGyrY1/numOfData
    meanGyrZ1 = sumGyrZ1/numOfData
    meanGyrX2 = sumGyrX2/numOfData
    meanGyrY2 = sumGyrY2/numOfData
    meanGyrZ2 = sumGyrZ2/numOfData
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)

    peakAccX1 = chicken.accx1[i]
    peakAccY1 = chicken.accy1[i]
    peakAccZ1 = chicken.accz1[i]
    peakAccX2 = chicken.accx2[i]
    peakAccY2 = chicken.accy2[i]
    peakAccZ2 = chicken.accz2[i]
    peakGyrX1 = chicken.gyrx1[i]
    peakGyrY1 = chicken.gyry1[i]
    peakGyrZ1 = chicken.gyrz1[i]
    peakGyrX2 = chicken.gyrx2[i]
    peakGyrY2 = chicken.gyry2[i]
    peakGyrZ2 = chicken.gyrz2[i]
    
    for a in range(numOfData):
        if(chicken.accx1[i+a] > peakAccX1):
            peakX = chicken.accx1[i+a]
        if(chicken.accy1[i+a] > peakAccY1):
            peakY = chicken.accy1[i+a]
        if(chicken.accz1[i+a] > peakAccZ1):
            peakZ = chicken.accz1[i+a]
        if(chicken.accx2[i+a] > peakAccX2):
            peakX = chicken.accx2[i+a]
        if(chicken.accy2[i+a] > peakAccY2):
            peakY = chicken.accy2[i+a]
        if(chicken.accz2[i+a] > peakAccZ2):
            peakZ = chicken.accz2[i+a]
        if(chicken.gyrx1[i+a] > peakGyrX1):
            peakX = chicken.gyrx1[i+a]
        if(chicken.gyry1[i+a] > peakGyrY1):
            peakY = chicken.gyry1[i+a]
        if(chicken.gyrz1[i+a] > peakGyrZ1):
            peakZ = chicken.gyrz1[i+a]
        if(chicken.gyrx2[i+a] > peakGyrX2):
            peakX = chicken.gyrx2[i+a]
        if(chicken.gyry2[i+a] > peakGyrY2):
            peakY = chicken.gyry2[i+a]
        if(chicken.gyrz2[i+a] > peakGyrZ2):
            peakZ = chicken.gyrz2[i+a]
            
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    labels.append(3)
    features.append(feature)
    feature = []
    
    if( (i + overlapNum) > (numRowsOfChicken - numOfData)):
        break
    else:
        i = i + overlapNum

j=0
numRowsOfnumber7 = number7.shape[0]

for line in number7.iterrows():
    
    sumAccX1 = 0
    sumAccY1 = 0
    sumAccZ1 = 0
    sumAccX2 = 0
    sumAccY2 = 0
    sumAccZ2 = 0
    sumGyrX1 = 0
    sumGyrY1 = 0
    sumGyrZ1 = 0
    sumGyrX2 = 0
    sumGyrY2 = 0
    sumGyrZ2 = 0
    
    for index in range(numOfData):
        sumAccX1 = sumAccX1 + number7.accx1[j+index]
        sumAccY1 = sumAccY1 + number7.accy1[j+index]
        sumAccZ1 = sumAccZ1 + number7.accz1[j+index]
        sumAccX2 = sumAccX2 + number7.accx2[j+index]
        sumAccY2 = sumAccY2 + number7.accy2[j+index]
        sumAccZ2 = sumAccZ2 + number7.accz2[j+index]
        sumGyrX1 = sumGyrX1 + number7.gyrx1[j+index]
        sumGyrY1 = sumGyrY1 + number7.gyry1[j+index]
        sumGyrZ1 = sumGyrZ1 + number7.gyrz1[j+index]
        sumGyrX2 = sumGyrX2 + number7.gyrx2[j+index]
        sumGyrY2 = sumGyrY2 + number7.gyry2[j+index]
        sumGyrZ2 = sumGyrZ2 + number7.gyrz2[j+index]
    
    meanAccX1 = sumAccX1/numOfData
    meanAccY1 = sumAccY1/numOfData
    meanAccZ1 = sumAccZ1/numOfData
    meanAccX2 = sumAccX2/numOfData
    meanAccY2 = sumAccY2/numOfData
    meanAccZ2 = sumAccZ2/numOfData
    meanGyrX1 = sumGyrX1/numOfData
    meanGyrY1 = sumGyrY1/numOfData
    meanGyrZ1 = sumGyrZ1/numOfData
    meanGyrX2 = sumGyrX2/numOfData
    meanGyrY2 = sumGyrY2/numOfData
    meanGyrZ2 = sumGyrZ2/numOfData
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)

    peakAccX1 = number7.accx1[j]
    peakAccY1 = number7.accy1[j]
    peakAccZ1 = number7.accz1[j]
    peakAccX2 = number7.accx2[j]
    peakAccY2 = number7.accy2[j]
    peakAccZ2 = number7.accz2[j]
    peakGyrX1 = number7.gyrx1[j]
    peakGyrY1 = number7.gyry1[j]
    peakGyrZ1 = number7.gyrz1[j]
    peakGyrX2 = number7.gyrx2[j]
    peakGyrY2 = number7.gyry2[j]
    peakGyrZ2 = number7.gyrz2[j]
    
    for a in range(numOfData):
        if(number7.accx1[j+a] > peakAccX1):
            peakX = number7.accx1[j+a]
        if(number7.accy1[j+a] > peakAccY1):
            peakY = number7.accy1[j+a]
        if(number7.accz1[j+a] > peakAccZ1):
            peakZ = number7.accz1[j+a]
        if(number7.accx2[j+a] > peakAccX2):
            peakX = number7.accx2[j+a]
        if(number7.accy2[j+a] > peakAccY2):
            peakY = number7.accy2[j+a]
        if(number7.accz2[j+a] > peakAccZ2):
            peakZ = number7.accz2[j+a]
        if(number7.gyrx1[j+a] > peakGyrX1):
            peakX = number7.gyrx1[j+a]
        if(number7.gyry1[j+a] > peakGyrY1):
            peakY = number7.gyry1[j+a]
        if(number7.gyrz1[j+a] > peakGyrZ1):
            peakZ = number7.gyrz1[j+a]
        if(number7.gyrx2[j+a] > peakGyrX2):
            peakX = number7.gyrx2[j+a]
        if(number7.gyry2[j+a] > peakGyrY2):
            peakY = number7.gyry2[j+a]
        if(number7.gyrz2[j+a] > peakGyrZ2):
            peakZ = number7.gyrz2[j+a]
            
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    labels.append(2)
    features.append(feature)
    feature =[]
    
    if( (j + overlapNum) > (numRowsOfnumber7 - numOfData)):
        break
    else:
        j = j + overlapNum
        
k=0
numRowsOfsidestep = sidestep.shape[0]

for line in sidestep.iterrows():
    
    sumAccX1 = 0
    sumAccY1 = 0
    sumAccZ1 = 0
    sumAccX2 = 0
    sumAccY2 = 0
    sumAccZ2 = 0
    sumGyrX1 = 0
    sumGyrY1 = 0
    sumGyrZ1 = 0
    sumGyrX2 = 0
    sumGyrY2 = 0
    sumGyrZ2 = 0
    
    for index in range(numOfData):
        sumAccX1 = sumAccX1 + sidestep.accx1[k+index]
        sumAccY1 = sumAccY1 + sidestep.accy1[k+index]
        sumAccZ1 = sumAccZ1 + sidestep.accz1[k+index]
        sumAccX2 = sumAccX2 + sidestep.accx2[k+index]
        sumAccY2 = sumAccY2 + sidestep.accy2[k+index]
        sumAccZ2 = sumAccZ2 + sidestep.accz2[k+index]
        sumGyrX1 = sumGyrX1 + sidestep.gyrx1[k+index]
        sumGyrY1 = sumGyrY1 + sidestep.gyry1[k+index]
        sumGyrZ1 = sumGyrZ1 + sidestep.gyrz1[k+index]
        sumGyrX2 = sumGyrX2 + sidestep.gyrx2[k+index]
        sumGyrY2 = sumGyrY2 + sidestep.gyry2[k+index]
        sumGyrZ2 = sumGyrZ2 + sidestep.gyrz2[k+index]
    
    meanAccX1 = sumAccX1/numOfData
    meanAccY1 = sumAccY1/numOfData
    meanAccZ1 = sumAccZ1/numOfData
    meanAccX2 = sumAccX2/numOfData
    meanAccY2 = sumAccY2/numOfData
    meanAccZ2 = sumAccZ2/numOfData
    meanGyrX1 = sumGyrX1/numOfData
    meanGyrY1 = sumGyrY1/numOfData
    meanGyrZ1 = sumGyrZ1/numOfData
    meanGyrX2 = sumGyrX2/numOfData
    meanGyrY2 = sumGyrY2/numOfData
    meanGyrZ2 = sumGyrZ2/numOfData
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)

    peakAccX1 = sidestep.accx1[k]
    peakAccY1 = sidestep.accy1[k]
    peakAccZ1 = sidestep.accz1[k]
    peakAccX2 = sidestep.accx2[k]
    peakAccY2 = sidestep.accy2[k]
    peakAccZ2 = sidestep.accz2[k]
    peakGyrX1 = sidestep.gyrx1[k]
    peakGyrY1 = sidestep.gyry1[k]
    peakGyrZ1 = sidestep.gyrz1[k]
    peakGyrX2 = sidestep.gyrx2[k]
    peakGyrY2 = sidestep.gyry2[k]
    peakGyrZ2 = sidestep.gyrz2[k]
    
    for a in range(numOfData):
        if(sidestep.accx1[k+a] > peakAccX1):
            peakX = sidestep.accx1[k+a]
        if(sidestep.accy1[k+a] > peakAccY1):
            peakY = sidestep.accy1[k+a]
        if(sidestep.accz1[k+a] > peakAccZ1):
            peakZ = sidestep.accz1[k+a]
        if(sidestep.accx2[k+a] > peakAccX2):
            peakX = sidestep.accx2[k+a]
        if(sidestep.accy2[k+a] > peakAccY2):
            peakY = sidestep.accy2[k+a]
        if(sidestep.accz2[k+a] > peakAccZ2):
            peakZ = sidestep.accz2[k+a]
        if(sidestep.gyrx1[k+a] > peakGyrX1):
            peakX = sidestep.gyrx1[k+a]
        if(sidestep.gyry1[k+a] > peakGyrY1):
            peakY = sidestep.gyry1[k+a]
        if(sidestep.gyrz1[k+a] > peakGyrZ1):
            peakZ = sidestep.gyrz1[k+a]
        if(sidestep.gyrx2[k+a] > peakGyrX2):
            peakX = sidestep.gyrx2[k+a]
        if(sidestep.gyry2[k+a] > peakGyrY2):
            peakY = sidestep.gyry2[k+a]
        if(sidestep.gyrz2[k+a] > peakGyrZ2):
            peakZ = sidestep.gyrz2[k+a]
        
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    labels.append(4)
    features.append(feature)
    feature =[]
    
    if( (k + overlapNum) > (numRowsOfsidestep - numOfData)):
        break
    else:
        k = k + overlapNum
        
l=0
numRowsOfwipers = wipers.shape[0]

for line in wipers.iterrows():
    
    sumAccX1 = 0
    sumAccY1 = 0
    sumAccZ1 = 0
    sumAccX2 = 0
    sumAccY2 = 0
    sumAccZ2 = 0
    sumGyrX1 = 0
    sumGyrY1 = 0
    sumGyrZ1 = 0
    sumGyrX2 = 0
    sumGyrY2 = 0
    sumGyrZ2 = 0
    
    for index in range(numOfData):
        sumAccX1 = sumAccX1 + wipers.accx1[l+index]
        sumAccY1 = sumAccY1 + wipers.accy1[l+index]
        sumAccZ1 = sumAccZ1 + wipers.accz1[l+index]
        sumAccX2 = sumAccX2 + wipers.accx2[l+index]
        sumAccY2 = sumAccY2 + wipers.accy2[l+index]
        sumAccZ2 = sumAccZ2 + wipers.accz2[l+index]
        sumGyrX1 = sumGyrX1 + wipers.gyrx1[l+index]
        sumGyrY1 = sumGyrY1 + wipers.gyry1[l+index]
        sumGyrZ1 = sumGyrZ1 + wipers.gyrz1[l+index]
        sumGyrX2 = sumGyrX2 + wipers.gyrx2[l+index]
        sumGyrY2 = sumGyrY2 + wipers.gyry2[l+index]
        sumGyrZ2 = sumGyrZ2 + wipers.gyrz2[l+index]
    
    meanAccX1 = sumAccX1/numOfData
    meanAccY1 = sumAccY1/numOfData
    meanAccZ1 = sumAccZ1/numOfData
    meanAccX2 = sumAccX2/numOfData
    meanAccY2 = sumAccY2/numOfData
    meanAccZ2 = sumAccZ2/numOfData
    meanGyrX1 = sumGyrX1/numOfData
    meanGyrY1 = sumGyrY1/numOfData
    meanGyrZ1 = sumGyrZ1/numOfData
    meanGyrX2 = sumGyrX2/numOfData
    meanGyrY2 = sumGyrY2/numOfData
    meanGyrZ2 = sumGyrZ2/numOfData
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)

    peakAccX1 = wipers.accx1[l]
    peakAccY1 = wipers.accy1[l]
    peakAccZ1 = wipers.accz1[l]
    peakAccX2 = wipers.accx2[l]
    peakAccY2 = wipers.accy2[l]
    peakAccZ2 = wipers.accz2[l]
    peakGyrX1 = wipers.gyrx1[l]
    peakGyrY1 = wipers.gyry1[l]
    peakGyrZ1 = wipers.gyrz1[l]
    peakGyrX2 = wipers.gyrx2[l]
    peakGyrY2 = wipers.gyry2[l]
    peakGyrZ2 = wipers.gyrz2[l]
    
    for a in range(numOfData):
        if(wipers.accx1[l+a] > peakAccX1):
            peakX = wipers.accx1[l+a]
        if(wipers.accy1[l+a] > peakAccY1):
            peakY = wipers.accy1[l+a]
        if(wipers.accz1[l+a] > peakAccZ1):
            peakZ = wipers.accz1[l+a]
        if(wipers.accx2[l+a] > peakAccX2):
            peakX = wipers.accx2[l+a]
        if(wipers.accy2[l+a] > peakAccY2):
            peakY = wipers.accy2[l+a]
        if(wipers.accz2[l+a] > peakAccZ2):
            peakZ = wipers.accz2[l+a]
        if(wipers.gyrx1[l+a] > peakGyrX1):
            peakX = wipers.gyrx1[l+a]
        if(wipers.gyry1[l+a] > peakGyrY1):
            peakY = wipers.gyry1[l+a]
        if(wipers.gyrz1[l+a] > peakGyrZ1):
            peakZ = wipers.gyrz1[l+a]
        if(wipers.gyrx2[l+a] > peakGyrX2):
            peakX = wipers.gyrx2[l+a]
        if(wipers.gyry2[l+a] > peakGyrY2):
            peakY = wipers.gyry2[l+a]
        if(wipers.gyrz2[l+a] > peakGyrZ2):
            peakZ = wipers.gyrz2[l+a]
            
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    labels.append(1)
    features.append(feature)
    feature =[]
    
    if( (l + overlapNum) > (numRowsOfwipers - numOfData)):
        break
    else:
        l = l + overlapNum

m=0
numRowsOfturnclap = turnclap.shape[0]

for line in turnclap.iterrows():
    
    sumAccX1 = 0
    sumAccY1 = 0
    sumAccZ1 = 0
    sumAccX2 = 0
    sumAccY2 = 0
    sumAccZ2 = 0
    sumGyrX1 = 0
    sumGyrY1 = 0
    sumGyrZ1 = 0
    sumGyrX2 = 0
    sumGyrY2 = 0
    sumGyrZ2 = 0
    
    for index in range(numOfData):
        sumAccX1 = sumAccX1 + turnclap.accx1[m+index]
        sumAccY1 = sumAccY1 + turnclap.accy1[m+index]
        sumAccZ1 = sumAccZ1 + turnclap.accz1[m+index]
        sumAccX2 = sumAccX2 + turnclap.accx2[m+index]
        sumAccY2 = sumAccY2 + turnclap.accy2[m+index]
        sumAccZ2 = sumAccZ2 + turnclap.accz2[m+index]
        sumGyrX1 = sumGyrX1 + turnclap.gyrx1[m+index]
        sumGyrY1 = sumGyrY1 + turnclap.gyry1[m+index]
        sumGyrZ1 = sumGyrZ1 + turnclap.gyrz1[m+index]
        sumGyrX2 = sumGyrX2 + turnclap.gyrx2[m+index]
        sumGyrY2 = sumGyrY2 + turnclap.gyry2[m+index]
        sumGyrZ2 = sumGyrZ2 + turnclap.gyrz2[m+index]
    
    meanAccX1 = sumAccX1/numOfData
    meanAccY1 = sumAccY1/numOfData
    meanAccZ1 = sumAccZ1/numOfData
    meanAccX2 = sumAccX2/numOfData
    meanAccY2 = sumAccY2/numOfData
    meanAccZ2 = sumAccZ2/numOfData
    meanGyrX1 = sumGyrX1/numOfData
    meanGyrY1 = sumGyrY1/numOfData
    meanGyrZ1 = sumGyrZ1/numOfData
    meanGyrX2 = sumGyrX2/numOfData
    meanGyrY2 = sumGyrY2/numOfData
    meanGyrZ2 = sumGyrZ2/numOfData
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)

    peakAccX1 = turnclap.accx1[m]
    peakAccY1 = turnclap.accy1[m]
    peakAccZ1 = turnclap.accz1[m]
    peakAccX2 = turnclap.accx2[m]
    peakAccY2 = turnclap.accy2[m]
    peakAccZ2 = turnclap.accz2[m]
    peakGyrX1 = turnclap.gyrx1[m]
    peakGyrY1 = turnclap.gyry1[m]
    peakGyrZ1 = turnclap.gyrz1[m]
    peakGyrX2 = turnclap.gyrx2[m]
    peakGyrY2 = turnclap.gyry2[m]
    peakGyrZ2 = turnclap.gyrz2[m]
    
    for a in range(numOfData):
        if(turnclap.accx1[m+a] > peakAccX1):
            peakX = turnclap.accx1[m+a]
        if(turnclap.accy1[m+a] > peakAccY1):
            peakY = turnclap.accy1[m+a]
        if(turnclap.accz1[m+a] > peakAccZ1):
            peakZ = turnclap.accz1[m+a]
        if(turnclap.accx2[m+a] > peakAccX2):
            peakX = turnclap.accx2[m+a]
        if(turnclap.accy2[m+a] > peakAccY2):
            peakY = turnclap.accy2[m+a]
        if(turnclap.accz2[m+a] > peakAccZ2):
            peakZ = turnclap.accz2[m+a]
        if(turnclap.gyrx1[m+a] > peakGyrX1):
            peakX = turnclap.gyrx1[m+a]
        if(turnclap.gyry1[m+a] > peakGyrY1):
            peakY = turnclap.gyry1[m+a]
        if(turnclap.gyrz1[m+a] > peakGyrZ1):
            peakZ = turnclap.gyrz1[m+a]
        if(turnclap.gyrx2[m+a] > peakGyrX2):
            peakX = turnclap.gyrx2[m+a]
        if(turnclap.gyry2[m+a] > peakGyrY2):
            peakY = turnclap.gyry2[m+a]
        if(turnclap.gyrz2[m+a] > peakGyrZ2):
            peakZ = turnclap.gyrz2[m+a]
            
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    labels.append(5)
    features.append(feature)
    feature =[]
    
    if( (m + overlapNum) > (numRowsOfturnclap - numOfData)):
        break
    else:
        m = m + overlapNum
        
n=0
numRowsOfneutral = neutral.shape[0]

for line in neutral.iterrows():
    
    sumAccX1 = 0
    sumAccY1 = 0
    sumAccZ1 = 0
    sumAccX2 = 0
    sumAccY2 = 0
    sumAccZ2 = 0
    sumGyrX1 = 0
    sumGyrY1 = 0
    sumGyrZ1 = 0
    sumGyrX2 = 0
    sumGyrY2 = 0
    sumGyrZ2 = 0
    
    for index in range(numOfData):
        sumAccX1 = sumAccX1 + neutral.accx1[n+index]
        sumAccY1 = sumAccY1 + neutral.accy1[n+index]
        sumAccZ1 = sumAccZ1 + neutral.accz1[n+index]
        sumAccX2 = sumAccX2 + neutral.accx2[n+index]
        sumAccY2 = sumAccY2 + neutral.accy2[n+index]
        sumAccZ2 = sumAccZ2 + neutral.accz2[n+index]
        sumGyrX1 = sumGyrX1 + neutral.gyrx1[n+index]
        sumGyrY1 = sumGyrY1 + neutral.gyry1[n+index]
        sumGyrZ1 = sumGyrZ1 + neutral.gyrz1[n+index]
        sumGyrX2 = sumGyrX2 + neutral.gyrx2[n+index]
        sumGyrY2 = sumGyrY2 + neutral.gyry2[n+index]
        sumGyrZ2 = sumGyrZ2 + neutral.gyrz2[n+index]
    
    meanAccX1 = sumAccX1/numOfData
    meanAccY1 = sumAccY1/numOfData
    meanAccZ1 = sumAccZ1/numOfData
    meanAccX2 = sumAccX2/numOfData
    meanAccY2 = sumAccY2/numOfData
    meanAccZ2 = sumAccZ2/numOfData
    meanGyrX1 = sumGyrX1/numOfData
    meanGyrY1 = sumGyrY1/numOfData
    meanGyrZ1 = sumGyrZ1/numOfData
    meanGyrX2 = sumGyrX2/numOfData
    meanGyrY2 = sumGyrY2/numOfData
    meanGyrZ2 = sumGyrZ2/numOfData
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)

    peakAccX1 = neutral.accx1[m]
    peakAccY1 = neutral.accy1[m]
    peakAccZ1 = neutral.accz1[m]
    peakAccX2 = neutral.accx2[m]
    peakAccY2 = neutral.accy2[m]
    peakAccZ2 = neutral.accz2[m]
    peakGyrX1 = neutral.gyrx1[m]
    peakGyrY1 = neutral.gyry1[m]
    peakGyrZ1 = neutral.gyrz1[m]
    peakGyrX2 = neutral.gyrx2[m]
    peakGyrY2 = neutral.gyry2[m]
    peakGyrZ2 = neutral.gyrz2[m]
    
    for a in range(numOfData):
        if(neutral.accx1[n+a] > peakAccX1):
            peakX = neutral.accx1[n+a]
        if(neutral.accy1[n+a] > peakAccY1):
            peakY = neutral.accy1[n+a]
        if(neutral.accz1[n+a] > peakAccZ1):
            peakZ = neutral.accz1[n+a]
        if(neutral.accx2[n+a] > peakAccX2):
            peakX = neutral.accx2[n+a]
        if(neutral.accy2[n+a] > peakAccY2):
            peakY = neutral.accy2[n+a]
        if(neutral.accz2[n+a] > peakAccZ2):
            peakZ = neutral.accz2[n+a]
        if(neutral.gyrx1[n+a] > peakGyrX1):
            peakX = neutral.gyrx1[n+a]
        if(neutral.gyry1[n+a] > peakGyrY1):
            peakY = neutral.gyry1[n+a]
        if(neutral.gyrz1[n+a] > peakGyrZ1):
            peakZ = neutral.gyrz1[n+a]
        if(neutral.gyrx2[n+a] > peakGyrX2):
            peakX = neutral.gyrx2[n+a]
        if(neutral.gyry2[n+a] > peakGyrY2):
            peakY = neutral.gyry2[n+a]
        if(neutral.gyrz2[n+a] > peakGyrZ2):
            peakZ = neutral.gyrz2[n+a]
            
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    labels.append(0)
    features.append(feature)
    feature =[]
    
    if( (n + overlapNum) > (numRowsOfneutral - numOfData)):
        break
    else:
        n = n + overlapNum
        
FEATURES = features
LABELS = labels

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(FEATURES,LABELS,test_size=0.1,random_state=1)

from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(solver = 'lbfgs', activation ='tanh', hidden_layer_sizes= (500,))

from sklearn.model_selection import cross_val_score

scores = cross_val_score(mlp, x_train, y_train, cv = 5)
print(scores)
mlp.fit(x_train,y_train)

from sklearn.externals import joblib
joblib.dump(mlpr, "MLP.cls")

#RanFor1 = joblib.load("RanFor.cls")

#from sklearn.metrics import *

#print('accurary_train =', accuracy_score(y_train, RanFor.predict(x_train)))
#print('accuracy_test =', accuracy_score(y_test, model.predict(x_test)))
#print('precision =', precision_score(y_test, model.predict(x_test)))
#print('recall =', recall_score(y_test, model.predict(x_test)))
#print('score =', f1_score(y_test, model.predict(x_test)))






