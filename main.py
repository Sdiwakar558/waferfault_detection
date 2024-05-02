import os.path
import shutil

from Client_Raw_Data_Validation.Raw_Data_Validation import Raw_data_validations


class maincalling_function:
    def __init__(self):
        self.raw_data_validation = Raw_data_validations()

    def call_preocedure(self):
        if os.path.exists("./Training_Log/Raw_Data_Validation.txt"):
            os.remove("./Training_Log/Raw_Data_Validation.txt")
        log_file = open("./Training_Log/Raw_Data_Validation.txt",'w')
        log_file.write("Raw_Data_Validation")
        log_file.close()
        print(self.raw_data_validation.creating_copy_of_complete_data())
        schema_data = self.raw_data_validation.fetchdatafrom_schema_training()

        manual_regex = self.raw_data_validation.manualregex()
        self.raw_data_validation.read_training_batchfolder(manual_regex)
        print(manual_regex)
        NumberofColumns = schema_data[3]
        print(self.raw_data_validation.validate_file_columndetails(NumberofColumns))
        self.raw_data_validation.validateMissingValueInWholeColumn()




if __name__ == "__main__":
    maincalling_function().call_preocedure()
