# Leakage Detection Web App

## Overview

Welcome to the Leakage Detection Web App! This is a Python-based web application that allows you to input data and receive model predictions for the leakages in a vacuum bags used in the manufacture of carbon fibre reinforced parts. Whether you're new to the app or a returning user, this guide will help you get started.

## Features

- Input data: You can provide input data related to mass flow through vacuum pumps.
- Select Flight: Choose the aircraft model (e.g., A320, A380) to specify the context for the prediction. Based on the aircraft model chosen, the app will communicate with the appropriate model hosted on tensorflow serving docker.
- Receive Predictions: The app will process your input and provide predictions for leakage coordinates.
- Visualization: View a graphical representation of the leakage location on a wing contour plot.

## Getting Started

Follow these steps to use the Leakage Detection Web App:

1. **Install Docker**: Make sure you have Docker installed on your system.
2. **create Docker Image**: You can create a Docker image for your web app using the provided Dockerfile and the following command:
    docker build -t dlr_web_app:latest .
3. **Docker compose up**: Run docker container by 
    docker-compose up 

### Alternative
3. **Run Docker container**:
   docker run -d -p 8000:8000 --name=leak_det_web_app dlr_web_app:latest

4. **Run the app locally**: http://127.0.0.1:8000/


## Input Data
1. Select a Flight Model: Choose the aircraft model from the dropdown list (e.g., A320, A380).

2. Enter Mass Flow: Provide mass flow values for vacuum pumps. The number of inputs required may vary depending on the selected flight model.

    Note: You may need to enter default values for some pumps based on the selected flight model.
    Viewing Predictions
3. Once you submit your input, the app will process it and provide you with predictions for leakage coordinates. You can view the predicted leakage location on a graphical plot of the wing contour.

## Troubleshooting
1. If you encounter any issues or have questions, please feel free to contact us. @sreerag.office@gmail.com
2. Make sure Docker is correctly configured and running on your system.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Enjoy using the Leakage Detection Web App! If you find it helpful or have suggestions for improvements, we'd love to hear from you.


#### internal
Feedback on the coding practice.
Testing: It's important to include testing for your application to ensure it functions as expected. If you haven't done so, consider adding unit tests and possibly integration tests to cover different parts of your application.

Logging: Consider implementing logging for your application. It can help with debugging and monitoring the application in production.

Security: Depending on the nature of your application and the data it handles, consider security best practices, such as input validation, securing sensitive data, and following Flask security recommendations.

