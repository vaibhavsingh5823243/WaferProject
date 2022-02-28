from appLogger import app_logger
from nullHandler import data_tranformation
from attributesValidator import datavalidation_param
from dboperation import dboperation
from sklearn.model_selection import train_test_split
import pandas as pd
from dataProcessing.preprocessing import Preprocessing
from bestModelFinder.model_tuner import ModelTuner
from objectSaver.save_model import SaveModel
class Train:

    """
    This class will run the all the code like,datapreprocessing,data
    validation,data transformation dboperation,objectSaver training etc.
    """
    def __init__(self):
        self.log = app_logger.AppLogger()
        self.processing = Preprocessing()
        self.modelTuner = ModelTuner()
        self.objSaver = SaveModel()
        self.data_transfrm = data_tranformation.DataTransform()
        self.data_val = datavalidation_param.Validation_DSA('rawFolder\\')
        self.db = dboperation.DBOperation('s', 'validatedFiles\\Good_Raw_Files\\', 'validatedFiles\\Bad_Raw_Files\\')


    def train(self):
        try:
            data = pd.read_csv("trainingDir\\input.csv")
            data = self.processing.dropColumns(data,['Wafer'])
            feature,target = self.processing.seperateLables(data,'Output')
            colsWithZeroStd = self.processing.getColumnsWithZeroSD(feature)
            feature = self.processing.dropColumns(feature,colsWithZeroStd)
            if self.processing.isNullPresent(feature):
                feature = self.processing.imputeMissingValues(data)
            xTrain,xTest,yTrain,yTest = train_test_split(feature,target,random_state=58,train_size=.90)
            model,modelName = self.modelTuner.getBestModel(xTrain,yTrain,xTest,yTest)
            self.objSaver.save_model(model,modelName)
            message = f"Model training done successfully.\nBest model is {modelName}"
            self.log.logger(message)
        except Exception as e:
            self.log.logger(str(e))

    def startTraining(self):
        try:
            # self.log.logger("Script Started...")
            # filename,len_datestamp,len_timestamp,num_cols,col_names = self.data_val.getValidationValues()
            # regex = self.data_val.getRegex()
            # self.data_val.seperateBadAndGoodFiles(regex)
            # self.data_val.validateNumberOfColumns(num_cols)
            # self.data_transfrm.replaceMissingWithNull()
            # self.db.createTable('vaibhav',col_names)
            # self.db.insertIntoTable('vaibhav')
            # self.db.selectDataFromDbCsv('vaibhav','Good_Raw_Data')
            # self.log.logger("Data inserted into database.")
            self.train()
        except Exception as e:
            raise e
