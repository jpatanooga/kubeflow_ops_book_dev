from sklearn import datasets
import requests
iris = datasets.load_iris()
X, y = iris.data, iris.target
formData = {
    'instances': X[0:1].tolist()
}
res = requests.post('http://localhost:8080/v1/models/svm:predict', json=formData)
print(res)
print(res.text)