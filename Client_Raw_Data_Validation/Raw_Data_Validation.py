import shutil
import os
import pandas as pd
import json
import re
from App_Log_Writer.App_Logger import Logger

class Raw_data_validations:
    def __init__(self):
        self.schema_training_file = "./schema_training.json"
        self.good_raw_dest = "./Prediction_data/Good_Raw/"
        self.source = "./Training_Batch_Files/"
        self.copy_source = "./Training_batch_fileCopy/"
        self.bad_raw_dest = "./Prediction_data/Bad_Raw/"
        self.log_file = "./Training_Log/Raw_Data_Validation.txt"
        self.logwriter = Logger()

    def fetchdatafrom_schema_training(self):
        try:
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, "Taking data from schema_training.json STARTED")
            schema_training_json = open(self.schema_training_file)
            data = json.load(schema_training_json)
            SampleFileName = data['SampleFileName']
            LengthOfDateStampInFile = data['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = data['LengthOfTimeStampInFile']
            NumberofColumns = data['NumberofColumns']

            self.logwriter.log_writer(log_file,
                                      f"SampleFileName:{SampleFileName},LengthOfDateStampInFile:{LengthOfDateStampInFile},LengthOfTimeStampInFile:{LengthOfTimeStampInFile},NumberofColumns:{NumberofColumns}")
            log_file.close()
            return SampleFileName, LengthOfDateStampInFile,LengthOfTimeStampInFile, NumberofColumns
        except ValueError:
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, f"{ValueError} in fetchdatafrom_schema_training (Methods)")
            log_file.close()
        except KeyError:
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, f"{KeyError} in fetchdatafrom_schema_training (Methods)")
            log_file.close()
        except Exception as e:
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, f"{e} in fetchdatafrom_schema_training (Methods)")
            log_file.close()


    def manualregex(self):
        regex_val = r"wafer_\d{8}_\d{6}.csv"
        return regex_val

    def creating_copy_of_complete_data(self):
        try:
            log_file = open(self.log_file,'r+')
            self.logwriter.log_writer(log_file,"Copy training File started")
            if os.path.exists(self.copy_source):
                shutil.rmtree(self.copy_source)
            self.logwriter.log_writer(log_file, "Existing Training_Batch_fileCopy deleted successfully")
            shutil.copytree(self.source, self.copy_source)
            self.logwriter.log_writer(log_file, "Training file copied to Training_Batch_fileCopy")
            log_file.close()
        except Exception as e:
            log_file = open(self.log_file, 'a')
            self.logwriter.log_writer(log_file,f"{Exception} occured")


    def read_training_batchfolder(self, pattern):
        try:
            count = 0
            if os.path.exists(self.bad_raw_dest):
                os.rmdir(self.bad_raw_dest)
            else:
                os.makedirs(self.bad_raw_dest)
            if os.path.exists(self.good_raw_dest):
                os.rmdir(self.good_raw_dest)
            else:
                os.makedirs(self.good_raw_dest)
            for file in os.listdir(self.copy_source):
                if re.match(pattern,file):
                    count += 1
                    shutil.move(self.copy_source+file, self.good_raw_dest)
                else:
                    shutil.move(self.copy_source+file, self.bad_raw_dest)
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, f"{count} moved to Good_Raw")
            log_file.close()
        except OSError:
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, f"{OSError} occured")
            log_file.close()

        except Exception as e:
            log_file = open(self.log_file,'a')
            self.logwriter.log_writer(log_file, f"{e} occured")
            log_file.close()
    def validate_file_columndetails(self,NumberofColumns):
        try:
            log_file = open("./Training_Log/Raw_Data_Validation.txt","a+")
            self.logwriter.log_writer(log_file,"Column level validation started")
            for file in os.listdir(self.good_raw_dest):
                file_data_in_csv = pd.read_csv(self.good_raw_dest+file)
                if file_data_in_csv.shape[1] == NumberofColumns:
                    file_data_in_csv = file_data_in_csv.rename(columns={'Unnamed: 0':'wafer'})
                    file_data_in_csv.to_csv(self.good_raw_dest+file)
                else:
                    shutil.move(self.good_raw_dest+file,self.bad_raw_dest)
                    self.logwriter.log_writer(log_file, f"{file} moved to Bad_file folder")
            self.logwriter.log_writer(log_file,"Column validation completed")
            log_file.close()
        except OSError:
            log_file = open("./Training_Log/Raw_Data_Validation.txt","a+")
            self.logwriter.log_writer(log_file,f"{OSError} Ocurred")
            log_file.close()
        except Exception as e:
            log_file = open("./Training_Log/Raw_Data_Validation.txt","a+")
            self.logwriter.log_writer(log_file,f"{e} Ocurred")
            log_file.close()

    def validateMissingValueInWholeColumn(self):
        try:
            log_file = open("./Training_Log/Raw_Data_Validation.txt", "a+")
            self.logwriter.log_writer(log_file, "Column label validation started")
            for file in os.listdir(self.good_raw_dest):
                csv_data_file = pd.read_csv(self.good_raw_dest+file)
                for column in csv_data_file:
                    if len(csv_data_file[column])-csv_data_file[column].count() == len(csv_data_file[column]):
                        shutil.move(self.good_raw_dest+file,self.bad_raw_dest)
            self.logwriter.log_writer(log_file, "Column label validation completed")
            log_file.close()
        except OSError:
            log_file = open("./Training_Log/Raw_Data_Validation.txt","a+")
            self.logwriter.log_writer(log_file,f"{OSError} occured")
            log_file.close()
        except Exception as e:
            log_file = open("./Training_Log/Raw_Data_Validation.txt", "a+")
            self.logwriter.log_writer(log_file, f"{e} occured")
            log_file.close()