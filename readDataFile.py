import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_validate
from joblib import dump

def evaluate_classifiers(clfs, names, X, y):
    '''
    evaluate learning method for data X and y
    '''
    scores = {}
    best = None
    best_score = 0
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    resultat = []

    for clf, name in zip(clfs, names):
        
        tmpClfTrain = clf.fit(X_train, y_train)

        resultat.append([name,tmpClfTrain,tmpClfTrain.score(X_test, y_test)])
            
    print(resultat)

    for i in resultat:
        if (i[2]>0.9):
            dump(i[1], i[0]+'.joblib') 



def getMinMaxXY(fileName):
    """
    returns the minimum and maximum values of a column in the Excel file passed in parameter
    """
    df = pd.read_excel(fileName)
    
    df["ratioAxeX"] = (((df["eyeLeftLeftX"]+df["eyeRightRightX"])/df["topNoseX"])*1000)
    df["ratioAxeY"] = (df["bottomNoseY"]-df["topNoseY"])
    
    bornMinAxeX = df["ratioAxeX"].min()
    bornMaxAxeX = df["ratioAxeX"].max()
    bornMinAxeY = df["ratioAxeY"].min()
    bornMaxAxeY = df["ratioAxeY"].max()

    return (bornMinAxeX,bornMaxAxeX,bornMinAxeY,bornMaxAxeY)


def testLearning():
    '''
    function who try to learn data
    does not work with face data
    '''
    clfs = [DummyClassifier(strategy="stratified"),
            GaussianNB(), 
            # SVC(), 
            LogisticRegression(max_iter=10000), 
            DecisionTreeClassifier(criterion="entropy"),
            RandomForestClassifier()]

    names = ["Dummy", "GaussianNB", "SVC", "LogisticRegression", "DecisionTree", "RandomForest"]
    #names = ["Dummy", "GaussianNB", "LogisticRegression", "DecisionTree", "RandomForest"]


    X = pd.DataFrame(data=df["ratioAxeX"]) 
    y = pd.DataFrame(data=df["X"]) 

    #X = pd.DataFrame(data=df["ratioAxeY"]) 
    #y = pd.DataFrame(data=df["Y"]) 


    evaluate_classifiers(clfs, names, X, y)