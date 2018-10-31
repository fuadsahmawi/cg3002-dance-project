import pandas as pd

neutral = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\neutral.csv") #Label = 0
wipers = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\wipers.csv") #Label = 1
number7 = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\number7.csv") #label = 2
chicken = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\chicken.csv") #label = 3
sidestep = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\sidestep.csv") #Label = 4
turnclap = pd.read_csv(r"C:\Users\user\Desktop\CG3002 dataset\turnclap.csv") #Label = 5

labels = []
feature = []
numOfData = 10
overlapNum = 4
numRowsOfchicken = chicken.shape[0]
numRowsOfwipers = wipers.shape[0]
numRowsOfnumber7 = number7.shape[0]
numRowsOfturnclap = turnclap.shape[0]
numRowsOfsidestep = sidestep.shape[0]
numRowsOfneutral = neutral.shape[0]
mean_data = pd.DataFrame()
std_data = pd.DataFrame()
iqr_data = pd.DataFrame()

i=0

for line in chicken.iterrows():
    a = chicken[i:i+numOfData:].copy()
    a.loc['mean'] = a.mean()
    a.loc['std'] = a.std()
    Q3 = a.quantile(0.75)
    Q1 = a.quantile(0.25)
    a.loc['iqr'] = Q3 - Q1
    mean_data = mean_data.append(a.loc['mean'], ignore_index = True)
    std_data = std_data.append(a.loc['std'], ignore_index = True)
    iqr_data = iqr_data.append(a.loc['iqr'], ignore_index = True)
    
    if( (i + overlapNum) > (numRowsOfchicken - numOfData)):
        break
    else:
        i = i + overlapNum

mean_data = mean_data.rename(index=str, columns={'GyX 1': 'mean_GyX 1', 'GyY 1': 'mean_GyY 1', 'GyZ 1': 'mean_GyZ 1',
                                                 'AcX 1': 'mean_AcX 1', 'AcY 1': 'mean_AcY 1', 'AcZ 1': 'mean_AcZ 1',
                                                 'GyX 2': 'mean_GyX 2', 'GyY 2': 'mean_GyY 2', 'GyZ 2': 'mean_GyZ 2',
                                                 'AcX 2': 'mean_AcX 2', 'AcY 2': 'mean_AcY 2', 'AcZ 2': 'mean_AcZ 2', })
std_data = std_data.rename(index=str, columns=  {'AcX 1': 'std_AcX 1', 'AcY 1': 'std_AcY 1', 'AcZ 1': 'std_AcZ 1', 
                                                 'GyX 1': 'std_GyX 1', 'GyY 1': 'std_GyY 1', 'GyZ 1': 'std_GyZ 1',
                                                 'AcX 2': 'std_AcX 2', 'AcY 2': 'std_AcY 2', 'AcZ 2': 'std_AcZ 2', 
                                                 'GyX 2': 'std_GyX 2', 'GyY 2': 'std_GyY 2', 'GyZ 2': 'std_GyZ 2',})
iqr_data = iqr_data.rename(index=str, columns=  {'AcX 1': 'iqr_AcX 1', 'AcY 1': 'iqr_AcY 1', 'AcZ 1': 'iqr_AcZ 1', 
                                                 'GyX 1': 'iqr_GyX 1', 'GyY 1': 'iqr_GyY 1', 'GyZ 1': 'iqr_GyZ 1',
                                                 'AcX 2': 'iqr_AcX 2', 'AcY 2': 'iqr_AcY 2', 'AcZ 2': 'iqr_AcZ 2', 
                                                 'GyX 2': 'iqr_GyX 2', 'GyY 2': 'iqr_GyY 2', 'GyZ 2': 'iqr_GyZ 2',})

activity = mean_data['activity'].copy()
mean_data = mean_data.drop(['activity'], axis = 1)
std_data = std_data.drop(['activity'], axis = 1)
iqr_data = iqr_data.drop(['activity'], axis = 1)
chicken_extracted_data = mean_data.join(std_data)
chicken_extracted_data = chicken_extracted_data.join(iqr_data)
chicken_extracted_data['activity'] = activity
chicken_extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\chicken_extracted_dataset.csv',index=False)

i=0
mean_data = pd.DataFrame()
std_data = pd.DataFrame()
iqr_data = pd.DataFrame()

for line in neutral.iterrows():
    a = neutral[i:i+numOfData:].copy()
    a.loc['mean'] = a.mean()
    a.loc['std'] = a.std()
    Q3 = a.quantile(0.75)
    Q1 = a.quantile(0.25)
    a.loc['iqr'] = Q3 - Q1
    mean_data = mean_data.append(a.loc['mean'], ignore_index = True)
    std_data = std_data.append(a.loc['std'], ignore_index = True)
    iqr_data = iqr_data.append(a.loc['iqr'], ignore_index = True)
    
    if( (i + overlapNum) > (numRowsOfneutral - numOfData)):
        break
    else:
        i = i + overlapNum

mean_data = mean_data.rename(index=str, columns={'GyX 1': 'mean_GyX 1', 'GyY 1': 'mean_GyY 1', 'GyZ 1': 'mean_GyZ 1',
                                                 'AcX 1': 'mean_AcX 1', 'AcY 1': 'mean_AcY 1', 'AcZ 1': 'mean_AcZ 1',
                                                 'GyX 2': 'mean_GyX 2', 'GyY 2': 'mean_GyY 2', 'GyZ 2': 'mean_GyZ 2',
                                                 'AcX 2': 'mean_AcX 2', 'AcY 2': 'mean_AcY 2', 'AcZ 2': 'mean_AcZ 2', })
std_data = std_data.rename(index=str, columns=  {'AcX 1': 'std_AcX 1', 'AcY 1': 'std_AcY 1', 'AcZ 1': 'std_AcZ 1', 
                                                 'GyX 1': 'std_GyX 1', 'GyY 1': 'std_GyY 1', 'GyZ 1': 'std_GyZ 1',
                                                 'AcX 2': 'std_AcX 2', 'AcY 2': 'std_AcY 2', 'AcZ 2': 'std_AcZ 2', 
                                                 'GyX 2': 'std_GyX 2', 'GyY 2': 'std_GyY 2', 'GyZ 2': 'std_GyZ 2',})
iqr_data = iqr_data.rename(index=str, columns=  {'AcX 1': 'iqr_AcX 1', 'AcY 1': 'iqr_AcY 1', 'AcZ 1': 'iqr_AcZ 1', 
                                                 'GyX 1': 'iqr_GyX 1', 'GyY 1': 'iqr_GyY 1', 'GyZ 1': 'iqr_GyZ 1',
                                                 'AcX 2': 'iqr_AcX 2', 'AcY 2': 'iqr_AcY 2', 'AcZ 2': 'iqr_AcZ 2', 
                                                 'GyX 2': 'iqr_GyX 2', 'GyY 2': 'iqr_GyY 2', 'GyZ 2': 'iqr_GyZ 2',})

activity = mean_data['activity'].copy()
mean_data = mean_data.drop(['activity'], axis = 1)
std_data = std_data.drop(['activity'], axis = 1)
iqr_data = iqr_data.drop(['activity'], axis = 1)
neutral_extracted_data = mean_data.join(std_data)
neutral_extracted_data = neutral_extracted_data.join(iqr_data)
neutral_extracted_data['activity'] = activity
neutral_extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\neutral_extracted_dataset.csv',index=False)

i=0
mean_data = pd.DataFrame()
std_data = pd.DataFrame()
iqr_data = pd.DataFrame()

for line in wipers.iterrows():
    a = wipers[i:i+numOfData:].copy()
    a.loc['mean'] = a.mean()
    a.loc['std'] = a.std()
    Q3 = a.quantile(0.75)
    Q1 = a.quantile(0.25)
    a.loc['iqr'] = Q3 - Q1
    mean_data = mean_data.append(a.loc['mean'], ignore_index = True)
    std_data = std_data.append(a.loc['std'], ignore_index = True)
    iqr_data = iqr_data.append(a.loc['iqr'], ignore_index = True)
    
    if( (i + overlapNum) > (numRowsOfwipers - numOfData)):
        break
    else:
        i = i + overlapNum

mean_data = mean_data.rename(index=str, columns={'GyX 1': 'mean_GyX 1', 'GyY 1': 'mean_GyY 1', 'GyZ 1': 'mean_GyZ 1',
                                                 'AcX 1': 'mean_AcX 1', 'AcY 1': 'mean_AcY 1', 'AcZ 1': 'mean_AcZ 1',
                                                 'GyX 2': 'mean_GyX 2', 'GyY 2': 'mean_GyY 2', 'GyZ 2': 'mean_GyZ 2',
                                                 'AcX 2': 'mean_AcX 2', 'AcY 2': 'mean_AcY 2', 'AcZ 2': 'mean_AcZ 2', })
std_data = std_data.rename(index=str, columns=  {'AcX 1': 'std_AcX 1', 'AcY 1': 'std_AcY 1', 'AcZ 1': 'std_AcZ 1', 
                                                 'GyX 1': 'std_GyX 1', 'GyY 1': 'std_GyY 1', 'GyZ 1': 'std_GyZ 1',
                                                 'AcX 2': 'std_AcX 2', 'AcY 2': 'std_AcY 2', 'AcZ 2': 'std_AcZ 2', 
                                                 'GyX 2': 'std_GyX 2', 'GyY 2': 'std_GyY 2', 'GyZ 2': 'std_GyZ 2',})
iqr_data = iqr_data.rename(index=str, columns=  {'AcX 1': 'iqr_AcX 1', 'AcY 1': 'iqr_AcY 1', 'AcZ 1': 'iqr_AcZ 1', 
                                                 'GyX 1': 'iqr_GyX 1', 'GyY 1': 'iqr_GyY 1', 'GyZ 1': 'iqr_GyZ 1',
                                                 'AcX 2': 'iqr_AcX 2', 'AcY 2': 'iqr_AcY 2', 'AcZ 2': 'iqr_AcZ 2', 
                                                 'GyX 2': 'iqr_GyX 2', 'GyY 2': 'iqr_GyY 2', 'GyZ 2': 'iqr_GyZ 2',})

activity = mean_data['activity'].copy()
mean_data = mean_data.drop(['activity'], axis = 1)
std_data = std_data.drop(['activity'], axis = 1)
iqr_data = iqr_data.drop(['activity'], axis = 1)
wipers_extracted_data = mean_data.join(std_data)
wipers_extracted_data = wipers_extracted_data.join(iqr_data)
wipers_extracted_data['activity'] = activity
wipers_extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\wipers_extracted_dataset.csv',index=False)

i=0
mean_data = pd.DataFrame()
std_data = pd.DataFrame()
iqr_data = pd.DataFrame()

for line in number7.iterrows():
    a = number7[i:i+numOfData:].copy()
    a.loc['mean'] = a.mean()
    a.loc['std'] = a.std()
    Q3 = a.quantile(0.75)
    Q1 = a.quantile(0.25)
    a.loc['iqr'] = Q3 - Q1
    mean_data = mean_data.append(a.loc['mean'], ignore_index = True)
    std_data = std_data.append(a.loc['std'], ignore_index = True)
    iqr_data = iqr_data.append(a.loc['iqr'], ignore_index = True)
    
    if( (i + overlapNum) > (numRowsOfnumber7 - numOfData)):
        break
    else:
        i = i + overlapNum

mean_data = mean_data.rename(index=str, columns={'GyX 1': 'mean_GyX 1', 'GyY 1': 'mean_GyY 1', 'GyZ 1': 'mean_GyZ 1',
                                                 'AcX 1': 'mean_AcX 1', 'AcY 1': 'mean_AcY 1', 'AcZ 1': 'mean_AcZ 1',
                                                 'GyX 2': 'mean_GyX 2', 'GyY 2': 'mean_GyY 2', 'GyZ 2': 'mean_GyZ 2',
                                                 'AcX 2': 'mean_AcX 2', 'AcY 2': 'mean_AcY 2', 'AcZ 2': 'mean_AcZ 2', })
std_data = std_data.rename(index=str, columns=  {'AcX 1': 'std_AcX 1', 'AcY 1': 'std_AcY 1', 'AcZ 1': 'std_AcZ 1', 
                                                 'GyX 1': 'std_GyX 1', 'GyY 1': 'std_GyY 1', 'GyZ 1': 'std_GyZ 1',
                                                 'AcX 2': 'std_AcX 2', 'AcY 2': 'std_AcY 2', 'AcZ 2': 'std_AcZ 2', 
                                                 'GyX 2': 'std_GyX 2', 'GyY 2': 'std_GyY 2', 'GyZ 2': 'std_GyZ 2',})
iqr_data = iqr_data.rename(index=str, columns=  {'AcX 1': 'iqr_AcX 1', 'AcY 1': 'iqr_AcY 1', 'AcZ 1': 'iqr_AcZ 1', 
                                                 'GyX 1': 'iqr_GyX 1', 'GyY 1': 'iqr_GyY 1', 'GyZ 1': 'iqr_GyZ 1',
                                                 'AcX 2': 'iqr_AcX 2', 'AcY 2': 'iqr_AcY 2', 'AcZ 2': 'iqr_AcZ 2', 
                                                 'GyX 2': 'iqr_GyX 2', 'GyY 2': 'iqr_GyY 2', 'GyZ 2': 'iqr_GyZ 2',})

activity = mean_data['activity'].copy()
mean_data = mean_data.drop(['activity'], axis = 1)
std_data = std_data.drop(['activity'], axis = 1)
iqr_data = iqr_data.drop(['activity'], axis = 1)
number7_extracted_data = mean_data.join(std_data)
number7_extracted_data = number7_extracted_data.join(iqr_data)
number7_extracted_data['activity'] = activity
number7_extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\number7_extracted_dataset.csv',index=False)

i=0
mean_data = pd.DataFrame()
std_data = pd.DataFrame()
iqr_data = pd.DataFrame()

for line in sidestep.iterrows():
    a = sidestep[i:i+numOfData:].copy()
    a.loc['mean'] = a.mean()
    a.loc['std'] = a.std()
    Q3 = a.quantile(0.75)
    Q1 = a.quantile(0.25)
    a.loc['iqr'] = Q3 - Q1
    mean_data = mean_data.append(a.loc['mean'], ignore_index = True)
    std_data = std_data.append(a.loc['std'], ignore_index = True)
    iqr_data = iqr_data.append(a.loc['iqr'], ignore_index = True)
    
    if( (i + overlapNum) > (numRowsOfsidestep - numOfData)):
        break
    else:
        i = i + overlapNum

mean_data = mean_data.rename(index=str, columns={'GyX 1': 'mean_GyX 1', 'GyY 1': 'mean_GyY 1', 'GyZ 1': 'mean_GyZ 1',
                                                 'AcX 1': 'mean_AcX 1', 'AcY 1': 'mean_AcY 1', 'AcZ 1': 'mean_AcZ 1',
                                                 'GyX 2': 'mean_GyX 2', 'GyY 2': 'mean_GyY 2', 'GyZ 2': 'mean_GyZ 2',
                                                 'AcX 2': 'mean_AcX 2', 'AcY 2': 'mean_AcY 2', 'AcZ 2': 'mean_AcZ 2', })
std_data = std_data.rename(index=str, columns=  {'AcX 1': 'std_AcX 1', 'AcY 1': 'std_AcY 1', 'AcZ 1': 'std_AcZ 1', 
                                                 'GyX 1': 'std_GyX 1', 'GyY 1': 'std_GyY 1', 'GyZ 1': 'std_GyZ 1',
                                                 'AcX 2': 'std_AcX 2', 'AcY 2': 'std_AcY 2', 'AcZ 2': 'std_AcZ 2', 
                                                 'GyX 2': 'std_GyX 2', 'GyY 2': 'std_GyY 2', 'GyZ 2': 'std_GyZ 2',})
iqr_data = iqr_data.rename(index=str, columns=  {'AcX 1': 'iqr_AcX 1', 'AcY 1': 'iqr_AcY 1', 'AcZ 1': 'iqr_AcZ 1', 
                                                 'GyX 1': 'iqr_GyX 1', 'GyY 1': 'iqr_GyY 1', 'GyZ 1': 'iqr_GyZ 1',
                                                 'AcX 2': 'iqr_AcX 2', 'AcY 2': 'iqr_AcY 2', 'AcZ 2': 'iqr_AcZ 2', 
                                                 'GyX 2': 'iqr_GyX 2', 'GyY 2': 'iqr_GyY 2', 'GyZ 2': 'iqr_GyZ 2',})

activity = mean_data['activity'].copy()
mean_data = mean_data.drop(['activity'], axis = 1)
std_data = std_data.drop(['activity'], axis = 1)
iqr_data = iqr_data.drop(['activity'], axis = 1)
sidestep_extracted_data = mean_data.join(std_data)
sidestep_extracted_data = sidestep_extracted_data.join(iqr_data)
sidestep_extracted_data['activity'] = activity
sidestep_extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\sidestep_extracted_dataset.csv',index=False)

i=0
mean_data = pd.DataFrame()
std_data = pd.DataFrame()
iqr_data = pd.DataFrame()

for line in turnclap.iterrows():
    a = turnclap[i:i+numOfData:].copy()
    a.loc['mean'] = a.mean()
    a.loc['std'] = a.std()
    Q3 = a.quantile(0.75)
    Q1 = a.quantile(0.25)
    a.loc['iqr'] = Q3 - Q1
    mean_data = mean_data.append(a.loc['mean'], ignore_index = True)
    std_data = std_data.append(a.loc['std'], ignore_index = True)
    iqr_data = iqr_data.append(a.loc['iqr'], ignore_index = True)
    
    if( (i + overlapNum) > (numRowsOfturnclap - numOfData)):
        break
    else:
        i = i + overlapNum

mean_data = mean_data.rename(index=str, columns={'GyX 1': 'mean_GyX 1', 'GyY 1': 'mean_GyY 1', 'GyZ 1': 'mean_GyZ 1',
                                                 'AcX 1': 'mean_AcX 1', 'AcY 1': 'mean_AcY 1', 'AcZ 1': 'mean_AcZ 1',
                                                 'GyX 2': 'mean_GyX 2', 'GyY 2': 'mean_GyY 2', 'GyZ 2': 'mean_GyZ 2',
                                                 'AcX 2': 'mean_AcX 2', 'AcY 2': 'mean_AcY 2', 'AcZ 2': 'mean_AcZ 2', })
std_data = std_data.rename(index=str, columns=  {'AcX 1': 'std_AcX 1', 'AcY 1': 'std_AcY 1', 'AcZ 1': 'std_AcZ 1', 
                                                 'GyX 1': 'std_GyX 1', 'GyY 1': 'std_GyY 1', 'GyZ 1': 'std_GyZ 1',
                                                 'AcX 2': 'std_AcX 2', 'AcY 2': 'std_AcY 2', 'AcZ 2': 'std_AcZ 2', 
                                                 'GyX 2': 'std_GyX 2', 'GyY 2': 'std_GyY 2', 'GyZ 2': 'std_GyZ 2',})
iqr_data = iqr_data.rename(index=str, columns=  {'AcX 1': 'iqr_AcX 1', 'AcY 1': 'iqr_AcY 1', 'AcZ 1': 'iqr_AcZ 1', 
                                                 'GyX 1': 'iqr_GyX 1', 'GyY 1': 'iqr_GyY 1', 'GyZ 1': 'iqr_GyZ 1',
                                                 'AcX 2': 'iqr_AcX 2', 'AcY 2': 'iqr_AcY 2', 'AcZ 2': 'iqr_AcZ 2', 
                                                 'GyX 2': 'iqr_GyX 2', 'GyY 2': 'iqr_GyY 2', 'GyZ 2': 'iqr_GyZ 2',})

activity = mean_data['activity'].copy()
mean_data = mean_data.drop(['activity'], axis = 1)
std_data = std_data.drop(['activity'], axis = 1)
iqr_data = iqr_data.drop(['activity'], axis = 1)
turnclap_extracted_data = mean_data.join(std_data)
turnclap_extracted_data = turnclap_extracted_data.join(iqr_data)
turnclap_extracted_data['activity'] = activity
turnclap_extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\turnclap_extracted_dataset.csv',index=False)

frames = [neutral_extracted_data, wipers_extracted_data, number7_extracted_data, chicken_extracted_data, sidestep_extracted_data, turnclap_extracted_data]
extracted_data = pd.concat(frames)
extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\eryao_extracted_dataset.csv',index=False)
#extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\yupeng_extracted_dataset.csv',index=False)
#extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\fuad_extracted_dataset.csv',index=False)
#extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\melvin_extracted_dataset.csv',index=False)
#extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\ben_extracted_dataset.csv',index=False)
#extracted_data.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\xinhui_extracted_dataset.csv',index=False)

