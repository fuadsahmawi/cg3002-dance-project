import pandas as pd

extracted_features = pd.read_csv(r"C:\Users\User\Desktop\extracted_dataset.csv")

LABELS = extracted_features.activity

extracted_features = extracted_features.drop(["activity"], axis = 1)

FEATURES = extracted_features.values

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(FEATURES,LABELS,test_size=0.1,random_state=1)

from sklearn.ensemble import RandomForestClassifier
RanFor = RandomForestClassifier(n_estimators = 100, random_state =1)

from sklearn.model_selection import cross_val_score

scores = cross_val_score(RanFor, x_train, y_train, cv = 5)
print("RanFor: ")
print(scores)

from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(solver = 'lbfgs', activation ='relu', alpha=1e-5, hidden_layer_sizes= (500,))

scores = cross_val_score(mlp, x_train, y_train, cv = 5)
print("MLP: ")
print(scores)

from sklearn import svm

model = svm.SVC(kernel='linear')

scores = cross_val_score(model, x_train, y_train, cv = 5)
print("SVM: ")
print(scores)