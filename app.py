from flask import Flask, render_template, request
from utils.module import make_prediction

app = Flask(__name__)

min_limit = 0
max_limit = 1

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

                if not (min_limit <= input_value <= max_limit):
                    raise ValueError
                float_inputs.append(input_value)

            predictions = make_prediction(float_inputs)
            # total_sum = sum(float_inputs)
            # product_result = 1
            # for value in float_inputs:
            #     product_result *= value
            x_coords = predictions[0,0:1].tolist()[0]
            y_coords = predictions[0,1:2].tolist()[0]

            x_coords = "{:.2f}".format(x_coords)
            y_coords = "{:.2f}".format(y_coords)

            return render_template('result.html', enumerated_float_inputs=enumerate(float_inputs, 1),
                                   total_sum=x_coords, product_result=y_coords)
        except ValueError:
            error_message = "Invalid inputs. Please enter numbers between" +  str(min_limit) + " and " + str(max_limit)

        return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=None)

if __name__ == '__main__':
    app.run(debug=True)
