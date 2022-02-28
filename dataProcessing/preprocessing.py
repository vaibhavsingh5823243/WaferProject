import pandas as pd
import numpy as np
from appLogger import app_logger
from sklearn.impute import KNNImputer
from pandas_profiling import ProfileReport
from objectSaver.save_model import SaveModel
class Preprocessing:
    """
    This class is used for data preproccessing like
    handling null values ,label extraction,etc.
    """

    def __init__(self):
        self.log = app_logger.AppLogger()
        self.fileSaver = SaveModel()
    def dropColumns(self,data,columns):

        """This function will remove
           all the unnecessary columns
           from the data."""
        try:
            new_data = data.drop(columns=columns)
            message=f"Redundant columns {columns} removed successfully."
            self.log.logger(message)
            return new_data
        except Exception as e:
            self.log.logger(str(e))

    def seperateLables(self,data,lablename):
        """
        This function will seperate features and lable.
        :param data: datafile
        :param lablename: target values
        :return: feature and lables
        """
        try:
            feature =  data.drop(columns=[lablename])
            target = data[[lablename]]
            message=f"Features and target values seperated successfully.\nFeatures " \
                    f"are {feature.columns} and {lablename} is target value."
            self.log.logger(message)
            return feature,target
        except Exception as e:
            self.log.logger(str(e))

    def isNullPresent(self,data):
        """
        This function will check is there any null values
        exist.
        :param data: datafile
        :return:Boolean true or false
        """

        try:
            isnull=False
            null_count = data.isna().sum().sum()
            if null_count:
                isnull = True
            message = f"Null values checked successfully.{null_count} null values present in dataset."
            self.log.logger(message)
            return isnull
        except Exception as e:
            self.log.logger(str(e))

    def imputeMissingValues(self,data):
        """
        This function is used to fill all
        the null values using KNNimputer.
        :param data: dataset
        :return: newdata with no null values
        """
        try:
            imputer_obj = KNNImputer(n_neighbors=3,weights='uniform',missing_values=np.nan)
            new_data = imputer_obj.fit_transform(data)
            self.fileSaver.save_model(imputer_obj,"KNNImputer")
            new_data = pd.DataFrame(new_data,columns=data.columns)
            message = "Missing values imputed successfully."
            self.log.logger(message)
            return new_data
        except Exception as e:
            self.log.logger(str(e))

    def getColumnsWithZeroSD(self,data):
        """
        This function will return all the columns
        which have zero stadard deviation.
        :param data: dataset
        :return: list of columns with zero standard deviation.
        """
        try:
            data_info = data.describe()
            dropable_col = [col for col in data_info if data_info[col][2]==0]
            message = f"Columns with 0 standard deviation are:{dropable_col}"
            self.log.logger(message)
            return dropable_col
        except Exception as e:
            self.log.logger(str(e))

    def profileReport(self,prediction):
        try:
            report = ProfileReport(prediction)
            report.to_file('templates/report.html')
            string="Report Generated successfully."
            self.log.logger(string)
        except Exception as e:
            self.log.logger(str(e))


