import os
import pandas as pd
import csv
import sqlite3
from appLogger import app_logger


class DBOperation:

    def __init__(self,db_path,good_file_path,bad_file_path):
        self.db_path = ""#D:\\MachineLearningLiveClass\\baferdetection\\"#db_path
        self.good_file_path = good_file_path
        self.bad_file_path = bad_file_path
        self.log = app_logger.AppLogger()

    def getConnection(self,dbname):

        """
        This function will establish connection with database.
        :param dbname: database name
        :return: connection to database
        """
        try:
            conn = sqlite3.connect(dbname+'.db')
            self.log.logger(f"Successfully connected to {dbname} database.")
            return conn

        except Exception as e:
            self.log.logger(str(e))

    def createTable(self,dbname,columns,tbname='Good_Raw_Data'):

        """This function will create table if not
        exist .
        :param tbname:table name
        :return :None"""

        try:

            conn = self.getConnection(dbname)
            conn.execute(f"DROP TABLE IF EXISTS {tbname};")
            columns_nd_type=''
            for col in columns:
                columns_nd_type = columns_nd_type+','+col.replace(' - ','')+' '+columns[col]
            columns_nd_type = columns_nd_type[1:]
            conn.execute(f"CREATE TABLE IF NOT EXISTS {tbname} ({columns_nd_type})")
            self.log.logger(f"{tbname} successfully create inside {dbname} database.")

        except Exception as e:
            self.log.logger(str(e))

    def insertIntoTable(self,dbname,tbname='Good_Raw_Data'):

        """
        This function will insert all the
        file into table.
        :return:
        """
        try:
            connection = self.getConnection(dbname)

            for file in os.listdir(self.good_file_path):

                try:
                    with open(self.good_file_path + '\\' + file, "r") as f:
                        next(f)
                        csv_file = csv.reader(f, delimiter='\n')
                        for data in csv_file:
                            connection.execute(f"INSERT INTO {tbname} VALUES({data[0]})")
                            connection.commit()
                    message = f"{file} inserted into database successfully."
                    self.log.logger(message)

                except Exception as e:
                    self.log.logger(f"Error while insertion {file} data.")

            connection.close()
            self.log.logger(f"{dbname}Connection closed")

        except Exception as e:
            raise e

    def selectDataFromDbCsv(self,dbname,tbname,filename='input.csv'):
        """
        This function will read sql query and
        write data from database to csv
        :param dbname:database name
        :param tbname:tablename
        :return:
        """
        try:
            if not os.path.isdir('trainingDir'):
                os.makedirs(f'trainingDir/')
            input_file_path = 'trainingDir/'+filename
            connection = self.getConnection(dbname)
            query = f"SELECT * FROM {tbname}"
            csv_file = pd.read_sql_query(query,connection)
            csv_file.to_csv(input_file_path,index=False)
            message=f"Data fetched successfully from {tbname}"
            self.log.logger(message)
        except Exception as e:
            self.log.logger(str(e))
