import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from pandas import read_csv
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def validate_k(X_train, y_train):
    # creating odd list of K for KNN
    neighbors = list(range(1,10))

    # subsetting just the odd ones
    # advisible to take odd values for binary classification to avoid the ties 
    # i.e. two classes labels achieving the same score.
    #neighbors = list(filter(lambda x: x % 2 != 0, neighbors))

    cv_scores = [] # empty list that will hold cv scores

    # perform 10-fold cross validation for different values of k
    # each cross_val_score() runs the model through cv=10 times of training and testing
    # the mean scores of each k are then compared to find the most performant
    for k in neighbors:
        print("validating k = %d" % k)
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
        cv_scores.append(scores.mean())
        
    print("if scores deviate from mean, data is weird\n" + str(scores)) 
    print("cv_scores: " + str(cv_scores))

    # changing to misclassification error
    MSE = [1 - x for x in cv_scores]

    print("MSE: " + str(MSE.index(min(MSE))))

    # determining best k
    # lower error is better
    optimal_k = neighbors[MSE.index(min(MSE))]
    print("The optimal number of neighbors is %d" % optimal_k)

    # plot misclassification error vs k
    #plt.plot(neighbors, MSE)
    #plt.xlabel('Number of Neighbors K')
    #plt.ylabel('Misclassification Error')
    #plt.show()
    
    return optimal_k

# create design matrix X and target vector y
X_train =  read_csv('X_train.csv', header=0, index_col=None)
y_train =  np.ravel(read_csv('y_train.csv', header=0, index_col=None))
X_test =  read_csv('X_test.csv', header=0, index_col=None)
y_test =  read_csv('y_test.csv', header=0, index_col=None)

print("data loaded")

#optimal_k = validate_k(X_train, y_train)
optimal_k = 1

knn = KNeighborsClassifier(n_neighbors=optimal_k)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

acc = accuracy_score(y_test, pred)
cm = confusion_matrix(y_test, pred)

print(acc)
print(cm)

## output model to file
joblib.dump(knn, "knn_model")
