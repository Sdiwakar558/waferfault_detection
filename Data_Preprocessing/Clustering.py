import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from App_Log_Writer.App_Logger import Logger


class Create_Kmeans_Clustering:
    def __init__(self):
        self.logwriter = Logger()

    def elbow_plot(self,data):

        log_file = open("./Training_Log/Clustering.txt","a+")
        self.logwriter.log_writer(log_file,"elbow_plot started")
        wcss = []
        try:

            for i in range(1,11):
                kmeanscluster = KMeans(n_clusters=i,init='k-means++',random_state=42)
                kmeanscluster.fit(data)
                wcss.append(kmeanscluster.inertia_)

            plt.plot(range(1,11),wcss)
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.savefig("kmeans_elbo.png")

            kn = KneeLocator(range(1,11),wcss,curve='convex',direction='decreasing')


            self.logwriter.log_writer(log_file,"Plot is saved")
            log_file.close()
            return kn.knee
        except Exception as e:
            log_file = open("./Training_Log/Clustering.txt","a+")
            self.logwriter.log_writer(log_file,f"{e} error occurred")
            log_file.close()



    def create_cluster(self,data,Number_of_cluster):
        log_file = open("./Training_Log/Clustering.txt","a+")
        self.logwriter.log_writer(log_file,"Create cluster started")
        try:
            k_means = KMeans(n_clusters=Number_of_cluster,init='k-means++',random_state=42)
            cluster_data = k_means.fit_predict(data)
            data['Cluster'] =cluster_data
            print(data)
            print("data")
        except Exception as e:
            log_file = open("./Training_Log/Clustering.txt","a+")
            self.logwriter.log_writer(log_file,f"{e} occured check")
            log_file.close()


