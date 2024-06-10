import shutil
import pickle
import os
from App_Log_Writer.App_Logger import Logger

class File_operation:
    def __init__(self):
        self.Model_path = './Model'
        self.logger = Logger()

    def check_folderexistance(self):
        try:
            if os.path.exists(self.Model_path):
                # self.logger.log_writer(log_file, f'{self.Model_path} already exists')
                shutil.rmtree(self.Model_path)
                # self.logger.log_writer(log_file, f'{self.Model_path} deleted')
                os.mkdir(self.Model_path)
                # self.logger.log_writer(log_file, f'{self.Model_path} created')

            else:
                os.mkdir(self.Model_path)
                # self.logger.log_writer(log_file, 'save_model start')
        except Exception as e:
            raise e

    def save_model(self,Final_model,model_name):
        try:
            with open(self.Model_path+'/'+model_name+'.sav','wb') as f:
                pickle.dump(Final_model,f)

        except Exception as e:
            # log_file = open('./Training_Log/File_methods.txt')
            # self.logger.log_writer(log_file,'Log file created')
            # log_file.close()
            raise e
    def load_model(self,real_data):
        try:
            list_of_model = os.listdir(self.Model_path)

            for models in list_of_model:
                with open(self.Model_path+'/'+models,'rb') as f:
                    loaded_model = pickle.load(f)
                    predicted_data = loaded_model.predict(real_data)
                    print(predicted_data)
        except Exception as e:
            pass
            raise e