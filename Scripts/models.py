import numpy as np
from keras import layers
from keras.layers import Input, Add, Multiply, Subtract, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, Dropout, MaxPooling2D, GlobalMaxPooling2D
from keras.layers import Dense, Dropout, Input, Lambda, Flatten, Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.regularizers import l2
from keras.models import Model, load_model, Sequential
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
# from keras.utils import plot_model
#from resnets_utils import *
from keras.initializers import glorot_uniform, he_normal
import scipy.misc
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import keras.backend as K
K.set_image_data_format('channels_last') 
# K.set_learning_phase(1) 
import scipy
import cv2
from keras.layers import subtract
import keras
from keras.layers import Lambda
import tensorflow as tf 
from keras.optimizers import Adam,RMSprop   
def siamese(input_shape):
    model=Sequential()
    model.add(Conv2D(96, (11,11), activation='relu', name='conv11',input_shape=input_shape))
    model.add(BatchNormalization(epsilon=1e-06,  axis=1, momentum=0.9))
    model.add(MaxPooling2D((3,3), strides=(2, 2),padding='same'))    


    model.add(Conv2D(256, (5,5), activation='relu', name='conv12'))
    model.add(BatchNormalization(epsilon=1e-06,  axis=1, momentum=0.9))
    model.add(MaxPooling2D((3,3), strides=(2, 2),padding='same'))    
    model.add(Dropout(0.3))

    model.add(Conv2D(384, (3,3), activation='relu', name='conv13',input_shape=input_shape,padding='same'))
    model.add(Conv2D(256, (3,3), activation='relu', name='conv14'))
    model.add(MaxPooling2D((3,3), strides=(2, 2),padding='same'))
    model.add(Flatten())
    model.add(Dense(1024, kernel_regularizer=l2(0.0005), activation='relu', kernel_initializer=glorot_uniform(seed=0)))
    model.add(Dropout(0.3))
    model.add(Dense(128, kernel_regularizer=l2(0.0005), activation='relu', kernel_initializer=glorot_uniform(seed=0)))
    return model

def preprocess(img_input):
    img_input=cv2.resize(img_input,(220,155),interpolation=cv2.INTER_LINEAR )
#     img_input=cv2.bitwise_not(img_input)
    img_input=img_input/245
    return img_input

def euclidian(vects):
    X,y=vects
    return K.sqrt(K.sum(K.square(X-y),axis=1,keepdims=True))

def euclidean_distance_output_shape(shapes):
    shape1, shape2 = shapes
    return (shape1[0], 1)

def contrastive_loss(y, preds, margin=1):
	# explicitly cast the true class label data type to the predicted
	# class label data type (otherwise we run the risk of having two
	# separate data types, causing TensorFlow to error out)
	y = tf.cast(y, preds.dtype)
	# calculate the contrastive loss between the true labels and
	# the predicted labels
	squaredPreds = K.square(preds)
	squaredMargin = K.square(K.maximum(margin - preds, 0))
	loss = K.mean(y * squaredPreds + (1 - y) * squaredMargin)
	# return the computed contrastive loss to the calling function
	return loss

def build():
    apply_sigmodel = siamese((155,220,3))
    
    X_input1 = Input(shape=(155,220,3))
    X_input2 = Input(shape=(155,220,3)) 

    X_vect1 = apply_sigmodel(X_input1)
    X_vect2 = apply_sigmodel(X_input2)

    distance = Lambda(euclidian, output_shape=euclidean_distance_output_shape)([X_vect1,X_vect2])

    model = Model(inputs=[X_input1,X_input2], outputs=distance)

    rms = RMSprop(learning_rate=1e-4, rho=0.9, epsilon=1e-08)

    model.compile(loss=contrastive_loss,optimizer=rms,metrics=['accuracy'])

    return model    