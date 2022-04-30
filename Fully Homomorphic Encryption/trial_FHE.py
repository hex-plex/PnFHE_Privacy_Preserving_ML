from bfv.batch_encoder import BatchEncoder
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_evaluator import BFVEvaluator
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters

import pickle
from sklearn.decomposition import PCA
from mlxtend.data import loadlocal_mnist

X, y = loadlocal_mnist(
            images_path='t10k-images-idx3-ubyte', 
            labels_path='t10k-labels-idx1-ubyte')

ENC_SIZE = 128
N_CLASSES = 10

f = open("pca.pkl", "rb")
pca = pickle.load(f)
f.close()

X_d = pca.transform(X)

lin_matrx = np.load("lin_matrix.npz")['weight']

degree = ENC_SIZE

plain_modulus = ENC_SIZE*2 + 1

ciph_modulus = 8000000000000
params = BFVParameters(poly_degree=degree,
                        plain_modulus=plain_modulus,
                        ciph_modulus=ciph_modulus)
key_generator = BFVKeyGenerator(params)
public_key = key_generator.public_key
secret_key = key_generator.secret_key
relin_key = key_generator.relin_key
encoder = BatchEncoder(params)
encryptor = BFVEncryptor(params, public_key)
decryptor = BFVDecryptor(params, secret_key)
evaluator = BFVEvaluator(params)

pred = []
for img in X_d:
    plain1 = encoder.encode(img)
    ciph1 = encryptor.encrypt(plain1)
    class_dist = []
    for i in range(N_CLASSES):
        plain2 = encoder.encode(message2)
        ciph2 = encryptor.encrypt(lin_matrx[:, i])
        ciph_prod = evaluator.multiply(ciph1, ciph2, relin_key)
        decrypted_prod = decryptor.decrypt(ciph_prod)
        decoded_prod = encoder.decode(decrypted_prod)
        class_dist.append(sum(decoded_prod))
    pred.append(np.argmax(class_dist))

pred = np.array(pred)
print("Test Accuracy", (pred==y).sum()/len(y)*100)