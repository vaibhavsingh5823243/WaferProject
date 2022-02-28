from datetime import datetime,date

class AppLogger:

    def logger(self,messages):
        """
        This function will handle all the error inside project
        :param file_obj: it will take file object where error will be written.
        :param messages: Error message to write
        :return:
        """
        try:
            date_today=date.today()
            time=datetime.now()
            current_time=time.strftime('%H:%M:%S')
            with open('logFiles\\logFiles.txt','a+') as fO:
                fO.write("$"+str(date_today)+" "+str(current_time)+" "+messages+"\n")
        except OSError as s:
            raise s

        except Exception as e:
            raise e
