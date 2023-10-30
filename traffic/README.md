At first, I tried applying only one convolution layer and one pooling layer. After flattening the data, I used two hidden layers connected with a Dropout of 0.5 between each other and another Dropout between the second hidden layer and the output layer.

After this, I added one more convolution layer, but realized it was convenient for the second convolution layer to utilize more filters, as its inputs weren't direct image data but data that already went through a convolution stage, thus having more patterns to capture.

I was using a ReLU activation function for the output layer, but after realizing my model's accuracy was rather low, I googled about which activation function was the best for the output layer and learned that the "softmax" function is better suitable for our case, as we are dealing with a multiclass classification problem (because we have several exclusive classifications into which we'll group our data).

Finally, I realized that using only one hidden layer instead of two didn't hurt the model's accuracy, so I took the second hidden layer out.
