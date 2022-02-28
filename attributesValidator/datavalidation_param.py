import json
import re
import shutil
import os
import pandas as pd
from appLogger import app_logger
from dataProcessing import preprocessing
class Validation_DSA:

    def __init__(self,path):
        self.preprocessor = preprocessing.Preprocessing()
        self.batch_file_path = path
        self.log = app_logger.AppLogger()
        self.schema_path = "trainingDatasetSchema.json"

    def getValidationValues(self):

        """
        This function will fetch all the values which is required for Data Validation
        from prediction_schema file.
        :return: return all the values
        """

        try:
            self.log.logger(f"Fetching of values from {self.schema_path} started...")
            with open(self.schema_path,'r') as f:
                dictionary = json.load(f)
            filename = dictionary['SampleFileName']
            len_datestamp = dictionary['LengthOfDateStampInFile']
            len_timestamp = dictionary['LengthOfTimeStampInFile']
            num_cols = dictionary['NumberofColumns']
            col_names =  dictionary['ColName']
            messages = f"Values for validating Data Sharing Aggrement fetched successfully  from {self.schema_path}"
            self.log.logger(messages)
            return filename,len_datestamp,len_timestamp,num_cols,col_names

        except OSError:
            self.log.logger(OSError)

        except Exception as e:
            messages = f'We are facing some error while fetching data from {self.schema_path}'
            self.log.logger(messages)


    def getRegex(self):
        """
        This function will create a regex pattern for validating
        the files.
        :return: regex pattern
        """
        try:
            regex = "^(wafer_){1}\d{8}['_']{1}\d{6}(.csv)$"
            self.log.logger("Regex pattern created for file name validation purpose")
            return regex
        except Exception as e:
            self.log.logger(str(e))


    def createDirectoryForGoodBadFiles(self):

        """This function will create to seperate folder inside
           directory which will store good and bad files"""
        try:
            good_file_path = os.path.join('validatedFiles/','Good_Raw_Files/')
            if not os.path.isdir(good_file_path):
                os.makedirs(good_file_path)
                self.log.logger(f"{good_file_path} created.")
            bad_file_path = os.path.join("validatedFiles/",'Bad_Raw_Files/')
            if not os.path.isdir(bad_file_path):
                os.makedirs(bad_file_path)
            self.log.logger(f"{bad_file_path} created")
        except Exception as e:
            self.log.logger(str(e))


    def deleteGoodDataFile(self):
        """
        This function will delete the good data folder once all the file
        inside good data folder is uploaded to database to space optimization.
        :return:
        """
        try:
            path = 'validatedFiles/'
            if os.path.isdir(path+"Good_Raw_Files/"):
                shutil.rmtree(path+"Good_Raw_Files/")
                self.log.logger("Good Raw Folder deleted successfully.")

        except Exception as e:
            self.log.logger(str(e))


    def deleteBadFile(self):
        """
        This function will delete the Bad_File_Directory which contains
        all the bad files.
        :return:
        """
        try:
            path = "validatedFiles/"
            if os.path.isdir(path+"Bad_Raw_Files/"):
                shutil.rmtree(path+"Bad_Raw_Files/")
                self.log.logger("Bad Raw Folder deleted successfully.")

        except Exception as e:
            self.log.logger(str(e))


    def badFileArchieve(self):
        """
        This function will remove all the bad file from Bad Raw File folder
        to archieve folder for future reference.
        :return:
        """
        try:
            archive_path = "Archieve/"
            if not os.path.isdir(archive_path):
                os.makedirs(archive_path)

            source_folder = "validatedFiles/Bad_Raw_Files/"
            for file in os.listdir(source_folder):
                if file not in os.listdir(archive_path):
                    shutil.move(source_folder+file,archive_path)
                    self.log.logger(f"{file} moved to archived.")
            message = "All Bad files are moved to archive folder successfully."
            self.log.logger(message)

        except Exception as e:
            self.log.logger(str(e))


    def seperateBadAndGoodFiles(self,regex):#,len_of_timestamp,len_of_datestamp):
        """
        This function will read all the file from Raw File folder and
        divide it into good or bad file based on their name.
        :param regex: pattern of filename
        :param len_of_timestamp: length of timestamp
        :param len_of_datestamp: length of datestamp
        :return:
        """
        try:
            source_path = self.batch_file_path
            self.deleteBadFile()
            self.deleteGoodDataFile()
            self.createDirectoryForGoodBadFiles()
            good_destination = "validatedFiles//Good_Raw_Files//"
            bad_destination = "validatedFiles//Bad_Raw_Files//"
            for file in os.listdir(source_path):
                if re.match(pattern = regex,string = file):
                    shutil.copy(source_path+file,good_destination)
                    self.log.logger(f"{file} successfully moved to Good Raw Folder.")
                else:
                    shutil.copy(source_path+file,bad_destination)
                    self.log.logger(f"Bad file!! {file} move to Bad Raw Folder.")
            self.log.logger("All files are divided into Good Raw Files and Bad Raw Files.")

        except Exception as e:
            self.log.logger(str(e))


    def validateNullColumns(self,csv_file):

        """
        This function will take a csv file a input and return
        true if all the columns are not totally null otherwise
        return false.
        :param csv_file:
        :return: Boolean
        """
        try:
            for column in csv_file:
                if len(csv_file[column])-csv_file[column].count() == len(csv_file[column]):
                    return False
            return True

        except Exception as e:
            self.log.logger(str(e))


    def validateNumberOfColumns(self,num_cols):
        """This function will read all the file from Good Raw Folder and move it to
        Bad Raw Folder if validation is fails otherwise not."""

        try:
            self.log.logger("Column Validation Started...")
            for file in os.listdir("validatedFiles//Good_Raw_Files//"):
                csv_file=pd.read_csv("validatedFiles//Good_Raw_Files//"+file)
                # if self.preprocessor.isNullPresent(csv_file):
                #     csv_file = self.preprocessor.imputeMissingValues(csv_file)
                if csv_file.shape[1] == num_cols and self.validateNullColumns(csv_file):
                    csv_file.rename(columns={"Unnamed: 0":"Wafer"},inplace=True)
                    csv_file.to_csv("validatedFiles/Good_Raw_Files/"+file,header=True,index=None)
                    message = f"Number of columns and Null Columns" \
                              f"Validated successfully for {file}."
                    self.log.logger(message)
                else:
                     shutil.move("validatedFiles//Good_Raw_Files//"+file,"validatedFiles//Bad_Raw_Files//")
                     message=f"Column Validation fail for {file}"
                     self.log.logger(message)

        except OSError as s:
            self.log.logger(str(s))

        except Exception as e:
            self.log.logger(str(e))



