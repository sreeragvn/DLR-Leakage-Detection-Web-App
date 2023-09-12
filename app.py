from flask import Flask, render_template, request
from utils.module import make_prediction

app = Flask(__name__)

min_limit = 0
max_limit = 1

model_input_no = {
    "A380": 10,
    "A320": 9,
    "A300": 6,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        float_inputs = []
        error_message = None

        try:
            selected_flight = request.form.get('selected_flight', 'A380')  # Get the selected flight option with a default value of 'A380'
            # print(selected_flight)
            if selected_flight in model_input_no:
                num_iterations = model_input_no[selected_flight]
            # print(num_iterations)
            for i in range(1, num_iterations + 1):
                input_value = request.form.get(f'input{i}')
                if input_value is None or input_value.strip() == '':
                    input_value = 0.0
                else:
                    input_value = float(input_value)

                if not (min_limit <= input_value <= max_limit):
                    raise ValueError
                float_inputs.append(input_value)

            # work around for the time being for the code to work
            if selected_flight == 'A320':
                float_inputs.append(0.0)
            if selected_flight == 'A300':
                float_inputs.append(0.0)
                float_inputs.append(0.0)
                float_inputs.append(0.0)
                float_inputs.append(0.0)

            saved_inputs = float_inputs.copy()
            predictions = make_prediction(float_inputs, selected_flight)
            x_coords = predictions[0, 0:1].tolist()[0]
            y_coords = predictions[0, 1:2].tolist()[0]

            x_coords = "{:.2f}".format(x_coords)
            y_coords = "{:.2f}".format(y_coords)

            # print(num_iterations)
            return render_template('result.html', enumerated_float_inputs=enumerate(saved_inputs, 1),
                                   total_sum=x_coords, product_result=y_coords, selected_flight= selected_flight)
        except ValueError:
            error_message = f"Invalid inputs. Please enter numbers between {min_limit} and {max_limit}"

        return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
