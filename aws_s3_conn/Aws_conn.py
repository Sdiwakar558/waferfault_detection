import boto3
import os
class Aws_conn_est:
    def __init__(self):
        self.AWS_access_key_id = os.environ.get('AWS_Access_key_id')
        self.AWS_access_security_code = os.environ.get('AWS_Access_security_code')
    def aws_connest(self):
        client = boto3.client('s3',aws_access_key_id=self.AWS_access_key_id,
                              aws_secret_access_key=self.AWS_access_security_code)
        return client