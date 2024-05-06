import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import knee_locator
from App_Log_Writer.App_Logger import Logger

class Create_Kmeans_Clustering:
    def __init__(self):
        self.logwriter = Logger()

    def elbow_plot(self,data):
        log_file = open("./Training_Log/Clustering.txt","a+")
        self.logwriter.log_writer(log_file,"elbow_plot started")
        try:
            for i in range(1,11):
                kmeanscluster = KMeans(n_clusters=i,init = 'k_means++',random_state=42)
                kmeanscluster.fit()


        except Exception as e:
            pass


