import logging;
import os;


'''
	A class designed to print debugging information to a file called "all.log"

	Takes a string as input, in the format: "root/directory/"

	@author: Bradley Poulette
'''
class DebugLogger:
	
	def __init__(self, output_dir):
		self.path = output_dir;
		logger = logging.getLogger();

		# create console handler and set level to info
		handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w");
		handler.setLevel(logging.DEBUG);
		formatter = logging.Formatter("%(levelname)s - %(message)s");
		handler.setFormatter(formatter);
		logger.addHandler(handler);

	def writeToLog(self, text):
		logging.debug(text);


	