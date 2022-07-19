from distutils.command.build import build
from Scripts.models import build,preprocess
from keras.utils import load_img,img_to_array
import tensorflow as tf
import numpy as np
print("Num GPUs Available: ", len(tf.config.list_physical_devices('CPU')))
# from keras.utils import load_weights

class GetModel:
    def __init__(self):
        self.model=build()
        self.model.load_weights('D:\mdp_2\models\model_weights33.h5')
        self.threshold=0.5
    def predict_model(self,img_path1,img_path2):
        img1 = load_img(img_path1,target_size=(155,220)) 
        img2 = load_img(img_path2,target_size=(155,220))
        x = img_to_array(img1)
        l1=[x]
        x = img_to_array(img2)
        l2=[x]
        output=self.model.predict([np.asarray(l1),np.asarray(l2)])
        if output<self.threshold:
            return 1
        else:
            return 0







# img = load_img('D:/mdp_2/Images/temproary/forgeries_10_1.png',target_size=(155,220)) 
# x = img_to_array(img)
# print(x.shape)
# x=preprocess(x)
# print(x.shape)
# l1=[x]
# l2=[x]
# model.load_weights('D:\mdp_2\models\model_weights33.h5')

# print(model.predict([np.asarray(l1),np.asarray(l2)]))

