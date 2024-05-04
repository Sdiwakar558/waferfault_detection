import os.path
import shutil
from Upload_CSVTOS3.mearge_csv_for_s3 import upload_csv_to_s3
from Client_Raw_Data_Validation.Raw_Data_Validation import Raw_data_validations
from App_Log_Writer.App_Logger import Logger


class maincalling_function:
    def __init__(self):
        self.raw_data_validation = Raw_data_validations()
        self.upload_csv_to_s3 = upload_csv_to_s3()
        self.Logwriter = Logger()

    def call_preocedure(self):
        if os.path.exists("./Training_Log/main_process.txt"):
            os.remove("./Training_Log/main_process.txt")
        log_file = open("./Training_Log/main_process.txt", 'a+')
        self.Logwriter.log_writer(log_file,"Raw_Data_Validation.py   methods started")
        self.raw_data_validation.creating_copy_of_complete_data()
        schema_data = self.raw_data_validation.fetchdatafrom_schema_training()
        manual_regex = self.raw_data_validation.manualregex()
        self.raw_data_validation.read_training_batchfolder(manual_regex)
        NumberofColumns = schema_data[3]
        self.raw_data_validation.validate_file_columndetails(NumberofColumns)
        self.raw_data_validation.validateMissingValueInWholeColumn()
        self.Logwriter.log_writer(log_file, "Raw_Data_Validation.py   methods Completed")
#
#
# #               Above are the line which are responsible to call
# #               Raw_Data_Validation (file)
# #               of class
# #               Raw_data_validations
        self.Logwriter.log_writer(log_file,",merge_csv_for_s3.py      methods calling started")
        self.upload_csv_to_s3.mearge_all_csv()
        self.upload_csv_to_s3.upload_csv_s3()
        self.Logwriter.log_writer(log_file, ",merge_csv_for_s3.py      methods calling Completed")
        log_file.close()



if __name__ == "__main__":
    maincalling_function().call_preocedure()
