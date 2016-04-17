from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
iris = load_iris()

class RFClassifier():
	def __init__(self, pssmFeatures, isTTS, maxDepth = 5, numTree = 10):
        self.pssmFeatures = pssmFeatures
        self.isTTS = isTTS

	rf = RandomForestClassifier(maxDepth)
	self.predictor = rf.predict
	
idx = range(len(isTTS))
np.random.shuffle(idx)

rf.fit(iris.data[idx][:100], iris.target[idx][:100])


from sklearn.datasets import load_boston
boston = load_boston()
rf = RandomForestRegressor()
rf.fit(boston.data[:300], boston.target[:300])