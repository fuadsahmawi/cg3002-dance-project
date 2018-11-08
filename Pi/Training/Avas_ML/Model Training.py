import pandas as pd
from sklearn.metrics import accuracy_score

eryao_extracted_features = pd.read_csv(r"C:\Users\User\Desktop\CG3002 extracted features\eryao_extracted_dataset.csv")
#yupeng_extracted_features = pd.read_csv(r"C:\Users\User\Desktop\CG3002 extracted features\yupeng_extracted_dataset.csv")
#fuad_extracted_features = pd.read_csv(r"C:\Users\User\Desktop\CG3002 extracted features\fuad_extracted_dataset.csv")
melvin_extracted_features = pd.read_csv(r"C:\Users\User\Desktop\CG3002 extracted features\melvin_extracted_dataset.csv")
#ben_extracted_features = pd.read_csv(r"C:\Users\User\Desktop\CG3002 extracted features\ben_extracted_dataset.csv")
#xinhui_extracted_features = pd.read_csv(r"C:\Users\User\Desktop\CG3002 extracted features\xinhui_extracted_dataset.csv")

frames = [eryao_extracted_features, melvin_extracted_features]#, yupeng_extracted_features, fuad_extracted_features, ben_extracted_features, xinhui_extracted_features]
extracted_features = pd.concat(frames)
extracted_features.to_csv(r'C:\Users\User\Desktop\CG3002 extracted features\test_extracted_dataset.csv',index=False)

LABELS = extracted_features.activity

extracted_features = extracted_features.drop(["activity"], axis = 1)

FEATURES = extracted_features.values

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(FEATURES,LABELS,test_size=0.1,random_state=1)
#x_train = FEATURES
#y_train = LABELS
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

scaler.fit(x_train)
x_train = scaler.transform(x_train)
scaler.fit(x_test)
x_test = scaler.transform(x_test)

print("Start training")
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
RanFor = RandomForestClassifier(n_estimators = 100, random_state =1)

RanFor.fit(x_train,y_train)

scores = cross_val_score(RanFor, x_train, y_train, cv = 10)
print("RanFor: ")
print(scores)
print('accuracy_test =', accuracy_score(y_test, RanFor.predict(x_test)))
#print('accuracy_test =', accuracy_score(y_test, RanFor.predict(x_test)))
#print(RanFor.predict_proba(x_test))

#from sklearn.externals import joblib
#joblib.dump(RanFor, "RanFor.cls")

from sklearn.neural_network import MLPClassifier
#mlp = MLPClassifier(solver = 'lbfgs', activation ='relu', alpha=1e-5, hidden_layer_sizes= (300,200,100,50,40))

#mlp.fit(x_train,y_train)

#scores = cross_val_score(mlp, x_train, y_train, cv = 5)
print("MLP: ")
#print(scores)

#from sklearn.externals import joblib
#joblib.dump(mlp, "MLP.cls")

from sklearn import svm

model = svm.SVC(kernel='linear', probability = True)

model.fit(x_train,y_train)

scores = cross_val_score(model, x_train, y_train, cv = 10)
print("SVM: ")
print(scores)
print('accuracy_test =', accuracy_score(y_test, model.predict(x_test)))
#print(model.predict_proba(x_test))
#from sklearn.externals import joblib
#joblib.dump(model, "SVM.cls")


