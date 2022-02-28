import os
import shutil
import pickle
from appLogger import app_logger


class SaveModel:

    """
    This class is create for objectSaver
    saving and objectSaver loading.
    """

    def __init__(self):
        self.error_file = open("logFiles\\model_saving.txt","a+")
        self.model_dir = 'models\\'
        self.log = app_logger.AppLogger()

    def save_model(self,model,file):
         """
         This function will take objectSaver object and filename
         as parameter and save it.
         :param model:
         :param file:
         :return:
         """

         try:
             path = os.path.join(self.model_dir+file)
             if os.path.isdir(path):
                 shutil.rmtree(path)
                 os.makedirs(path)
             else:
                 os.makedirs(path)
             model_obj_path = os.path.join(path,file+'.sav')
             with open(model_obj_path,'wb') as f:
                 pickle.dump(model,f)
                 message = f"Model {file} saved successfully"
                 self.log.logger(message)

         except Exception as e:
             self.log.logger(str(e))

    def load_model(self,file):

        """This function will load
        save objectSaver for prediction."""

        try:
            model_obj_path = self.model_dir+'\\'+file+'\\'+file+ '.sav'
            with open(model_obj_path,'rb') as f:
                model = pickle.load(f)
                self.log.logger(f"{file} objectSaver load successfully.")
            return model

        except Exception as e:
            self.log.logger(str(e))
