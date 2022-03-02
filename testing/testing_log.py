import logging
import datetime
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')
logging.warning("Enetered topic is not in string format")
logging.error("error in topic")
