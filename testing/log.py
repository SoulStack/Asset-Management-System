import logging
import pyodbc
import time

logging.basicConfig(filename= "newfile.log",format = "%(asctime)s %(message)s",filemode = "w")

#creating an object

logger = logging.getLogger()

#setting the threshold of logger

logger.setLevel(logging.DEBUG)


def get() :
    t1 = time.time()
    server =  'soulasset.database.windows.net'
    database = "asset"
    username = "assetadmin"
    password = "Soulsvciot01"

    cnxn =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    logger.debug("connected to database")
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM History")
    row = cursor.fetchone()

    while row:
        print(row[1])
    row = cursor.fetchone()
    t2 = time.time()
    print("Total time taken{}".format(t2 - t1))

