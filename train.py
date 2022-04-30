from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle
from sklearn.decomposition import PCA
from mlxtend.data import loadlocal_mnist

X, y = loadlocal_mnist(
            images_path='train-images-idx3-ubyte', 
            labels_path='train-labels-idx1-ubyte')

ENC_SIZE = 128
N_CLASSES = 10

pca = PCA(n_components=ENC_SIZE)
pca.fit(X)

X_d = pca.transform(X)

f = open("pca.pkl", "wb")
pickle.dump(pca, f)
f.close()

lin_matrx = np.random.randn(ENC_SIZE, N_CLASSES)

one_hot = OneHotEncoder(sparse=False)
epochs = 1000
alpha = 0.01
for e in range(epochs):
    # print(X_d.shape, lin_matrx.shape)
    y_pred = X_d@lin_matrx
    y_pred = np.argmax(y_pred , axis=-1)
    acc = (y_pred==y).sum()/len(y_pred)*100
    yh = one_hot.fit_transform(y.reshape(-1,1))
    yh_pred = one_hot.transform(y_pred.reshape(-1,1)) 
    lin_matrx -= alpha*np.einsum("ij,kj->ij",lin_matrx, (yh_pred-yh))
    print("Training Accuracy at epoch", e, "is", acc)

np.savez_compressed("lin_matrix",weight=lin_matrx)
