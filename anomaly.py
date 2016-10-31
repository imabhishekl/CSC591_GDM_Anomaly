from os import listdir
from os.path import isfile, join

class Anomaly:
	file_path = None
	file_list = None
	def __init__(file_path):
		self.file_path = file_path

	def load_filename():
			self.file_list = [f for f in listdir(self.file_path) if isfile(join(self.file_path, f))]
