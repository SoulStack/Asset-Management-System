import logging
import datetime
class Log(object):
	"""docstring for Log"""
	def __init__(self,reader_log,):
		logging.basicConfig(filename="app.log",filemode='w', format='%(name)s - %(levelname)s - %(message)s')
		logging.warning('sample log: '+str(datetime.datetime.now()))
	def log1(self):
		logging.info("Sample log1: "+str(datetime.datetime.now()))

reader1=Log("reader1/library")
reader1.log1()
