import phe as ph
import json
import os.path
import cv2

def Generate_keys():
    keys={}
    public_key, private_key = ph.generate_paillier_keypair()
    keys['public_key'] = {'n': public_key.n}
    keys['private_key'] = {'p': private_key.p,'q':private_key.q}
    with open('priv_pub_KeyPair.json', 'w') as file:
        json.dump(keys, file)

def Fetch_keys():
    with open('priv_pub_KeyPair.json', 'r') as file:
        keys=json.load(file)
        pub_key=ph.PaillierPublicKey(n=int(keys['public_key']['n']))
        priv_key=ph.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
        return pub_key, priv_key

"""Encrypting Client data with public key"""
def Data_serialization(public_key, data):
    encrypted_data_list = [public_key.encrypt(x) for x in data]
    encrypted_data={}
    encrypted_data['public_key'] = {'n': public_key.n}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
    serialized = json.dumps(encrypted_data)
    return serialized    

# def get_image_data():
#     import numpy as np
#     from sklearn.decomposition import PCA
#     import gzip
#     f = gzip.open('train-images-idx3-ubyte.gz','r')

#     image_size = 28
#     num_images = 10000

#     # f.read(-1)
#     buf = f.read(image_size * image_size * num_images)
#     data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
#     data = data.reshape(num_images, image_size*image_size)
#     print(data.shape)
#     pca = PCA(n_components=32)
#     pca.fit(data)
#     reduced_img = pca.transform(data[10].ravel().reshape(1,-1))
#     # from  sklearn.preprocessing import MinMaxScaler
#     # scaler = MinMaxScaler()
#     # reduced_img = scaler.fit_transform(img.ravel().reshape(1,-1))
#     import pdb; pdb.set_trace()
#     return reduced_img.ravel()



if not os.path.exists('priv_pub_KeyPair.json'):
    Generate_keys()

# if not os.path.exists('Client_data.json'):
pub_key, priv_key = Fetch_keys()
data = [2012, 25000, 1, 1, 1, 0]
datafile = Data_serialization(pub_key, data)
with open('Client_data.json', 'w') as file:
    json.dump(datafile, file)

if os.path.exists('prediction.json'):
    pub_key, priv_key = Fetch_keys()

    ##Load the result file returned by the server
    with open('prediction.json', 'r') as file:
        ans=json.load(file)
        answer_file=json.loads(ans)


    answer_key = ph.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
    answer = ph.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
    if (answer_key == pub_key):
        print(priv_key.decrypt(answer))
else:
    print("Waiting for Result")