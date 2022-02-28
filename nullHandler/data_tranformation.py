import os
import pandas as pd
from appLogger import app_logger

class DataTransform:

    def __init__(self,good_file_path='validatedFiles\\Good_Raw_Files\\'):
        self.file_path = good_file_path
        self.log = app_logger.AppLogger()

    def replaceMissingWithNull(self):
        """This function will replace all
           the missing value with null."""
        try:
            for file in os.listdir(self.file_path):
                csv_file=pd.read_csv(self.file_path+file)
                csv_file.fillna("NULL",inplace=True)
                csv_file['Wafer'] = csv_file['Wafer'].str[6:]
                csv_file.to_csv(self.file_path+file,header=True,index=None)
                self.log.logger(f"File {file} transformed successfully.")

        except Exception as e:
            self.log.logger(str(e))