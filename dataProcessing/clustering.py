from sklearn.cluster import KMeans
from kneed import KneeLocator
import matplotlib.pyplot as plt
from appLogger import app_logger
from objectSaver import save_model


class Clustering:

    def __init__(self):
        self.model_obj =save_model.SaveModel()
        self.log = app_logger.AppLogger()

    def elbow_plot(self,data):
        """
        This function will return optimum number of
        cluster
        :param data: dataset
        :return: number of cluster
        """
        try:
            wcss = []
            for i in range(1,11):
                kmean = KMeans(n_clusters=i,init='k-means++',random_state=58)
                kmean.fit(data)
                wcss.append(kmean.inertia_)
            """plt.plot(range(1,11),wcss)
            plt.title('Elbow Plot')
            plt.xlabel("Clusters")
            plt.ylabel("Within Cluster Summation of Square")
            plt.show()
            plt.savefig('elbow_plot.png')"""
            knee_obj = KneeLocator(range(1,11),wcss,curve='convex',direction='decreasing')
            optimum_cluster = knee_obj.knee
            message = f"Optimum number of clusters are:{optimum_cluster}"
            self.log.logger(message)
            return knee_obj.knee
        except Exception as e:
            self.log.logger(str(e))

    def createCluster(self,data,n_cluster):
        """
        This function will divide dataset into ncluster
        :param data: dataset
        :param n_cluster: no of cluster
        :return: newdataset along with their cluster
        """
        try:
            kmeans = KMeans(n_clusters=n_cluster,init='k-means++',random_state=58)
            y_clusters = kmeans.fit_predict(data)
            data['cluster'] = y_clusters
            self.model_obj.save_model(kmeans,'kmean')
            message = f"Dataset are divided into {n_cluster} clusters."
            self.log.logger(message)
            return data
        except Exception as e:
            self.log.logger(str(e))

