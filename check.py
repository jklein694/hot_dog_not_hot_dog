import tensorflow as tf
import os
import numpy as np
import cv2


def input_parser(filenames):

    tests = []

    for file_path in filenames:

        images = []
        image_size = 28
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Resizing the image to our desired size and
        # preprocessing will be done exactly as done during training
        image = cv2.resize(image, (image_size, image_size))
        images.append(image)
        images = np.array(images, dtype=np.uint8)
        images = images.astype('float32')

        images = images.ravel()
        X_check = images.reshape(-1, 784)

        tests.append(X_check)

    return X_check


def restore_model(tests, model_path):
    model_path = model_path

    y_correct = np.array([0.00000000, 1.000000000]).reshape(-1, 2)

    y_hats = []

    for test in tests:

        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(model_path + '.meta')
            saver.restore(sess, model_path)
            # access a variable from the saved Graph, and so on:

            graph = tf.get_default_graph()

            x = graph.get_tensor_by_name('x_placeholder:0')
            y = graph.get_tensor_by_name('y_placeholder:0')

            correct_prediction = graph.get_tensor_by_name('correct_prediction:0')

            y_hat = sess.run(correct_prediction, feed_dict={x: test, y: y_correct})

            y_hats.append(y_hat)

        return y_hats


def main():
    model_path = "saved_model/model.ckpt"
    file_path = ['hotdog.jpg', 'not_hotdog.jpg']
    image_check = input_parser(file_path)
    prediction = restore_model(image_check, model_path)

    for i in range(len(prediction)):
        print('Hotdog test')
        print('------------ \n')
        if prediction[i][0]:
            guess = 'Hotdog'
            print('This is a ', guess, '! My NN was right.')
        else:
            guess = 'not a hotdog'
            print('This is ', guess, ' and my NN was wrong.')
        print('\n')
        print('\n')

        print('Not hotdog test')
        print('--------------- \n')

        if prediction[i][0] == True:
            guess = 'Hotdog'
            print('This is a ', guess, ' :( My NN was wrong.')
        else:
            guess = 'not a hotdog'
            print('This is ', guess, ' and my NN was right!.')
        print('\n \n')


if __name__ == "__main__":
    main()
