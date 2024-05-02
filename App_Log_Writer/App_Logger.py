from datetime import datetime


class Logger:
    def __init__(self):
        self.curr_date_time = datetime.now()
        self.currdate = self.curr_date_time.date()
        self.currtime = self.curr_date_time.strftime("%H:%M:%S")

    def log_writer(self, file_obj, message):
        file_obj.write(f"{self.currdate}\t{self.currtime}\t\t\t{message}\n")
