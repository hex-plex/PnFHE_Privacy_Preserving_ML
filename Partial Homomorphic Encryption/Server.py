import json
import os.path
import phe as ph
import pandas as pd
from sklearn.linear_model import LinearRegression

""" Server will recieve encrypted data from the Client as
Client_data.json for the prediction. Server will apply the 
ML model and send back the predicted results back to Client."""    

class Linear_Regressor:

    def train_and_get_weights(self):
        df=pd.read_csv('./Data/Cars.csv')
        y=df['selling_price']
        X=df.drop('selling_price',axis=1)
        reg = LinearRegression().fit(X, y)
        return reg.coef_
        
def getPredictions():
    ## Load the encrypted data from the file
    with open('Client_data.json', 'r') as file:
        d = json.load(file)
    data = json.loads(d)

    ##Load the weights of trained ML model
    coeff = Linear_Regressor().train_and_get_weights()
    pk = data['public_key']
    public_key = ph.PaillierPublicKey(n=int(pk['n']))
    enc_nums_rec = [ph.EncryptedNumber(public_key, int(x[0], int(x[1]))) for x in data['values']]
    results = sum([coeff[i] * enc_nums_rec[i] for i in range(len(coeff))])
    return results, public_key

def main():
    if os.path.exists('Client_data.json'):
        if not os.path.exists('prediction.json'):
            results, public_key = getPredictions()
            datafile = serializeData(results, public_key)
            with open('prediction.json', 'w') as file:
                json.dump(datafile, file)
    print("Prediction file has been sent to the client.")

""" Now serilaize data ie encrypt data with public key and send back to Client"""
def serializeData(results, public_key):
    encrypted_data = {}
    encrypted_data['pubkey'] = {'n': public_key.n}
    encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
    serialized = json.dumps(encrypted_data)
    return serialized


if __name__ == '__main__':
    main()


