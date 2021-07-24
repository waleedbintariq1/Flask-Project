import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers,applications
from keras.applications.inception_v3 import preprocess_input



classes=['Cardiomegaly','COVID-19','Atelectasis','Effusion','Infiltration']
decoded =['Atelectasis','COVID-19','Cardiomegaly','Effusion','Infiltration']
image_size = (299, 299)
IMG_SIZE = 299

class Model:
    def __init__(self):
        self.model = keras.models.load_model('finalModel')
        self.data_gen = self.create_image_generator()

    lr = 0.0001


    def predict(self,filename):
        df = {
            'Images': [filename],
            'Labels': ['Atelectasis']}
        df = pd.DataFrame(df)

        test_X, test_Y = next(self.data_gen.flow_from_dataframe(dataframe=df,
                                                           directory=None,
                                                           x_col='Images',
                                                           y_col='Labels',
                                                           class_mode='categorical',
                                                           classes=classes,
                                                           target_size=image_size,
                                                           color_mode='rgb',
                                                           batch_size=1))

        pred = self.model.predict(test_X)
        return  self.hot_decoder(pred)

    def create_image_generator(self):
        core_idg = ImageDataGenerator(
        preprocessing_function=preprocess_input
        )
        return core_idg

    def hot_decoder(self,pred):
        predict = []

        max_no = -1000
        index = 0
        i = 0
        for a in pred[0]:
            a = float(a)

            predict.append(a)
            if a > max_no:
                max_no = a
                index = i
            i += 1
        print(predict)
        print("predicted", decoded[index])
        return decoded[index],max_no



# m = build_model(5)
# m.load_weights('InceptionV3ValAccuracyClasses_5.hdf5')
# m.save('inception_model_v1')


