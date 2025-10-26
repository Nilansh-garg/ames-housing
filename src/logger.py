import logging
import os
from datetime import datetime

# 1. Define the directory where all logs will be stored
LOG_DIR = os.path.join(os.getcwd(), "../../logs")

# 2. Define the name of the specific log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 3. Create the logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# 4. Define the final, complete file path
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)


logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)

if __name__=="__main__":
    logging.info("Logging has started")
    
    
    
    