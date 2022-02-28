from sklearn.decomposition import PCA
from appLogger import app_logger
from objectSaver.save_model import SaveModel
class Decomposition:
    """This class is used to decompose the
    value of dataset to less number of columns."""
    def __init__(self):
        self.log = app_logger.AppLogger()
        self.error_file = open('logFiles\\decomposition.txt', 'a+')
        self.model_saver = SaveModel()
    def fit_model(self,data,n_components=4):
        """
        This function will take data and
        return decomposite date.
        :param data:
        :return: decomposite data
        """
        try:
            pca = PCA(n_components=n_components)
            new_data = pca.fit_transform(data)
            self.model_saver.save_model(pca,'pca')
            self.log.logger("Data decomposite successfully.")
            return new_data
        except Exception as e:
            self.log.logger(str(e))
