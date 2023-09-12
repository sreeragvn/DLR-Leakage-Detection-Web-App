import json
import requests
import joblib
# import pandas as pd
import json
import requests
# import numpy as np
import matplotlib.pyplot as plt
import numpy as np

# MODEL_URL = 'http://localhost:8501/v1/models/single_leakage:predict'
MODEL_URL = 'http://localhost:8501/v1/models/leak_det:predict' # if running locally
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
   print(predictions)
   plot_test_pred(predictions[0])
   return predictions

x_range = np.arange(180, 16048, 250)
y_range = np.arange(100, 5233, 250)
X, Y = np.meshgrid(x_range, y_range)
def plot_test_pred(pred):
    plt.figure(figsize=(40, 20))
    
    # plt.title(f'Sample Number {sample_number}', fontsize=20)
    
    # plot sensor positions
    sensors = np.array([[2426, 70], [5480, 70], [8661, 191], [11676, 584], [13976, 917], [2603, 5163], [5723, 5163], [8417, 5103], [11646, 4740], [14641, 4391]])
    for i in range(len(sensors)):
        plt.scatter(sensors[i, 0], sensors[i, 1], color='tab:green', s=300)
        if i < 5:
            plt.text(sensors[i, 0], sensors[i, 1] - 200, 'MFC'+str(i+1), fontsize='xx-large')
        else:
            plt.text(sensors[i, 0], sensors[i, 1] + 350, 'MFC'+str(i+1), fontsize='xx-large')

    # plot leakage positions
    plt.scatter(X, Y, color='black', s=10)
    plt.scatter(pred[0], pred[1], color='tab:red', s=200)

    # print(X.shape)

    # plot wing contour
    plot_wing_contour()

    # include grid coordinate system
    plt.hlines(0, -1000, 17000, linestyle='dashed')
    plt.hlines(2600, -1000, 17000, linestyle='dashed')
    plt.hlines(5233, -1000, 17000, linestyle='dashed')
    plt.vlines(0, -1000, 6000, linestyle='dashed')
    plt.vlines(7930, -1000, 6000, linestyle='dashed')
    plt.vlines(16048, -1000, 6000, linestyle='dashed')
    plt.text(-850, -75, '$y = 0$', fontsize=20)
    plt.text(-850, 2600-75, '$y = 2600$', fontsize=20)
    plt.text(-850, 5233-75, '$y = 5233$', fontsize=20)
    plt.text(75, -700, '$x=0$', fontsize=20)
    plt.text(7930+75, -700, '$x=7930$', fontsize=20)
    plt.text(16048+75, -700, '$x=16048$', fontsize=20)
    # plt.text(180, 5800, f'(x1, y1) = ({x1}, {y1}) = ({j1-31}, {-i1+10})', fontsize=20)
    # invert y axis
    plt.gca().invert_yaxis()
    # plt.title("Leakage location")
    plt.savefig('./predictions_plot.png')

    # plt.show()

def plot_wing_contour():
    plt.plot([0, 7930], [0, 0], 'k')
    plt.plot([7930, 16048], [0, 1149], 'k')
    plt.plot([16048, 16048], [1149, 4386], 'k')
    plt.plot([16048, 7843], [4386, 5233], 'k')
    plt.plot([7843, 2493], [5233, 5233], 'k')
    plt.plot([2493, 0], [5233, 0], 'k')
    plt.xlim([-1000, 17000])
    plt.ylim([-1000, 6000])
    plt.xticks([])
    plt.yticks([])
    plt.gca().set_aspect('equal')