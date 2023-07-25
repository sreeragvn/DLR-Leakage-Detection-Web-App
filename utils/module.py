import json
import requests
import joblib
# import pandas as pd
import json
import requests
# import numpy as np

MODEL_URL = 'http://localhost:8501/v1/models/leak_det:predict'
scalar_path = './model/scalars/'
vacuum_pumps = ['MFC'+str(i) for i in range(1,11)]
# make sure that when you are scaling the data. it should've been a list - not numpy array or pandas dataframe
scaler_coords = joblib.load(scalar_path+'scaler_coords_list.save')
scaler_flows = joblib.load(scalar_path+'scaler_flows_list.save')

def interchange_list_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]

def preprocess_input(data):
    # COMMENT THE FOLLOWING 3 LINES ONCE YOU START TO TRAIN THE MODEL IN THE RIGHT ORDER OF VACUUM PUMPS
    for i in range(0,5):
        interchange_list_elements(data, i, i+5)
        interchange_list_elements(vacuum_pumps, i, i+5)
    # data = pd.DataFrame(data, index=vacuum_pumps).transpose()
    # print(data.shape)
    # data = np.array(data).reshape(-1,1).transpose()
    # print(data.shape)
    data = scaler_flows.transform([data])
    # print(data)
    return data.tolist()[0]
    # return data[0]

def postprocess_output(coords):
    # coords = np.array(coords).reshape(-1,1).transpose()
    coords = scaler_coords.inverse_transform([coords])
    return coords

def make_prediction(instances):
   instances = preprocess_input(instances)
#    print(instances)
   data = json.dumps({"signature_name": "serving_default", "instances": [instances]})
   headers = {"content-type": "application/json"}
   json_response = requests.post(MODEL_URL, data=data, headers=headers)
   predictions = json.loads(json_response.text)['predictions']
#    print(predictions)
   predictions = postprocess_output(predictions[0])
   return predictions

