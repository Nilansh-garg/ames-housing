import sys
from src.logger import logging

def error_message_detail(error, error_detail:sys):
    # Unpack the traceback object (exc_tb) from the sys.exc_info() tuple
    # Note: error_detail here is the 'sys' module you passed in the call.
    _, _, exc_tb = error_detail.exc_info() 
    
    # Extract details from the traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    # Construct the final error message
    # Note: Use f-string or .format() correctly, ensuring all three placeholders are used.
    error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"

    return error_message

class CustomException(Exception):
    def __init__(self,error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail= error_detail)
        
    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        a = 1/10
    except Exception as e:
        logging.info("Devide by zeri")
        raise CustomException(e,sys)
    