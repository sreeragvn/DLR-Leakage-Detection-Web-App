from flask import Flask, render_template, request
import json
import requests


app = Flask(__name__)

url = 'http://localhost:8501/v1/models/leak_det:predict'
def make_prediction(instances):
   data = json.dumps({"signature_name": "serving_default", "instances": [instances]})
   headers = {"content-type": "application/json"}
   json_response = requests.post(url, data=data, headers=headers)
   predictions = json.loads(json_response.text)['predictions']
   return predictions[0]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        float_inputs = []
        error_message = None

        try:
            for i in range(1, 11):
                input_value = request.form.get(f'input{i}')
                if input_value is None or input_value.strip() == '':
                    input_value = 0.0
                else:
                    input_value = float(input_value)

                if not (0 <= input_value <= 1):
                    raise ValueError
                float_inputs.append(input_value)

            predictions = make_prediction(float_inputs)
            # total_sum = sum(float_inputs)
            # product_result = 1
            # for value in float_inputs:
            #     product_result *= value
            total_sum = predictions[0]
            product_result = predictions[1]

            return render_template('result.html', enumerated_float_inputs=enumerate(float_inputs, 1),
                                   total_sum=total_sum, product_result=product_result)
        except ValueError:
            error_message = "Invalid inputs. Please enter numbers between 0 and 1."

        return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=None)

if __name__ == '__main__':
    app.run(debug=True)
