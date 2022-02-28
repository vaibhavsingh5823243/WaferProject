from appLogger import app_logger
from dataProcessing.preprocessing import Preprocessing
from objectSaver.save_model import SaveModel
import pandas as pd
from pca import Decomposition


class Prediction:

    def __init__(self):
        self.model_saver = SaveModel()
        self.log = app_logger.AppLogger()
        self.preprocessor = Preprocessing()
        self.pca = Decomposition()

    def predict(self,data):
        try:
            dataCol = list(data.columns)
            dataCol = [col.replace("-","") for col in dataCol]
            data.columns = dataCol;
            dataAttributes = pd.read_csv('trainingCols.csv')
            sensorId = list(data['Wafer'])
            data = data[list(dataAttributes.columns)]

            # if self.preprocessor.isNullPresent(data):
            #      imputer = self.model_saver.load_model('KNNImputer')
            #      data = imputer.transform(data)

            model = self.model_saver.load_model("XGBClassifier")
            y_pred = model.predict(data)
            result=[]

            for id,y in zip(sensorId,y_pred):
                if y==-1:
                    result.append([id,'Good'])
                else:
                    result.append([id,'Bad'])
            return result
        except Exception as e:
            raise e

