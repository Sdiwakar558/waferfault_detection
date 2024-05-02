import boto3
import pandas as pd
import os

class upload_csv_to_s3:
    def __init__(self):
        self.good_file_path = "./Prediction_data/Good_Raw/"
        self.S3_fileOBJ = "/waferfaultdatacsv/ML_DATASET/wafer_prediction.csv"

    def mearge_all_csv(self):
        for file in os.listdir(self.good_file_path):
            pd.read_csv(file)
    def upload_csv_s3(self):
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file()