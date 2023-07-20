import json
import requests

data = [-0.942463077854538, -0.623486361949005,     -0.134416678728349,     -0.213444983469962,       -0.303731398836841,     -0.696804741762093,     -0.362015716950389,     2.98274269995035,       0.608723261129162,      -0.403347537910888]

url = 'http://localhost:8501/v1/models/leak_det:predict'

# data_json = json.dumps({"instances": [data]})
# headers = {'content-type':'application/json'}
# json_response = requests.post(url, data=data_json, headers=headers)
# print(json_response.json())


def make_prediction(instances):
   data = json.dumps({"signature_name": "serving_default", "instances": [instances]})
   headers = {"content-type": "application/json"}
   json_response = requests.post(url, data=data, headers=headers)
   predictions = json.loads(json_response.text)['predictions']
   return predictions[0]

predictions = make_prediction(data)
print(predictions)  