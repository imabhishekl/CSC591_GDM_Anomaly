from os import listdir
from os.path import isfile, join
import numpy as np
import networkx as nx

class Anomaly:
	file_path = None
	file_list = None
	def __init__(self,file_path):
		self.file_path = file_path

	def load_filename(self):
			print "ad"
			self.file_list = [f for f in listdir(self.file_path) if isfile(join(self.file_path, f))]
			self.file_list = sorted(self.file_list,cmp=compare)
			print self.file_list

	def read(self):



def compare(file1,file2):
	return int(file1.split('_')[0]) - int(file2.split('_')[0])

def main():
	a = Anomaly("/home/abhishek/Downloads/anomaly/datasets/datasets/enron_by_day/")
	a.load_filename()

if __name__ == '__main__':
	main()