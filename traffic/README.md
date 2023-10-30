#Basic neural network
This is the sixth project of the course. It implements a very simple neural network using **TensorFlow** to to classify road signs based on an image of those signs, making use of a labeled dataset and using **OpenCV** to process the data before inputting it to the neural network.


## Data Set
The data set used in the course for this project can be downloaded from the following [link](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip). Once downloaded, move the resulting *gtsrb* directory inside the *traffic* directory.
## Dependencies for this project
run pip3 install -r requirements.txt to install this project’s dependencies: opencv-python for image processing, scikit-learn for ML-related functions, and tensorflow for neural networks.
## Usage
Run `python traffic.py gtsrb` on a terminal inside the project's folder, replacing **gtsrb** with any other dataset if needed.