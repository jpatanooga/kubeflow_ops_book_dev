from sklearn import svm
from sklearn import datasets
from joblib import dump
import joblib



filename = "/users/josh/Downloads/model.joblib"

print("Load Testing sklearn model from disk: " + filename)

iris_model = joblib.load(filename)
print( iris_model )


iris = datasets.load_iris()
X, y = iris.data, iris.target



#formData = {
#    'instances': X[0:1].tolist()
#}

print( X )

print( iris_model.score( X, y ) )

#print( iris_model.predict( X ) )