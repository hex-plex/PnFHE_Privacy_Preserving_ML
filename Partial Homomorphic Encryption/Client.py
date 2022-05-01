import phe as ph
import json
from os import path
from Server import Linear_Regressor 

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

## Generate Keys if not present already
if not path.exists('priv_pub_KeyPair.json'):
    Generate_keys()

## Fetch keys from file
pub_key, priv_key = Fetch_keys()

"""Encrypting Client data with public key"""
def Data_serialization(data, public_key):
    encrypted_data_list = [public_key.encrypt(x) for x in data]
    encrypted_data={}
    encrypted_data['public_key'] = {'n': public_key.n}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
    serialized = json.dumps(encrypted_data)
    return serialized   

## Sample data point to be predicted
data = [2012, 25000, 1, 1, 1, 0]
if not path.exists("Client_data.json"):
    datafile = Data_serialization(data, pub_key)
    with open('Client_data.json', 'w') as file:
        json.dump(datafile, file)

## Decrypting the data with private key
if not path.exists('prediction.json'):
    print("The prediction file has not been recieved from the server.")
else:
    pub_key, priv_key = Fetch_keys()

    ##Load the result file returned by the server
    with open('prediction.json', 'r') as file:
        ans=json.load(file)
        answer_file=json.loads(ans)

    answer_key = ph.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
    answer = ph.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
    if (answer_key == pub_key):
        print("Predicted Result after FHE:", priv_key.decrypt(answer))
    
    """ Verifying the result of Encryption Algorithm with original prediction."""
    data = [2012, 25000, 1, 1, 1, 0]
    Regressor_coeff = Linear_Regressor().train_and_get_weights()
    pred = sum([data[i]*Regressor_coeff[i] for i in range(len(data))])
    print("Original Predicted Result:", pred)