from os import listdir
from os.path import isfile, join
import numpy as np
import networkx as nx

class Anomaly:
	file_path = None
	file_list = None
	edge_lists = None
	vertices = None
	index = 0
	file_list_size = None

	def __init__(self,file_path):
		self.file_path = file_path

	def load_filename(self):			
			self.file_list = [f for f in listdir(self.file_path) if isfile(join(self.file_path, f))]
			self.file_list = sorted(self.file_list,cmp=compare)
			self.file_list_size = len(self.file_list)
			print self.file_list

	def loadEdgeVertices(self,index):
		if self.index == self.file_list_size:
			return
		file_name = self.file_list[index]
		graph_file = open(self.file_path + file_name)
		edges = graph_file.read().splitlines()
		self.vertices = range(int(edges[0].split(" ")[0]))
			
		self.edge_lists = map(lambda x:(int(x.split(" ")[0]),int(x.split(" ")[1])),edges[1:])
		print self.vertices
		print self.edge_lists

	def makeGraph(self):
		if self.index == self.file_list_size:
			return False
		self.loadEdgeVertices(self.index)
		G1 = nx.Graph()
		G1.add_nodes_from(self.vertices)
		G1.add_edges_from(self.edge_lists)
		self.loadEdgeVertices(self.index + 1)
		G2 = nx.Graph()
		G2.add_nodes_from(self.vertices)
		G2.add_edges_from(self.edge_lists)		
		self.index = self.index + 1
		A1,D1,max1 = self.makeDiagonal(G1)
		A2,D2,max2 = self.makeDiagonal(G2)
		return True

	def makeDiagonal(self,G):
		A = nx.adjacency_matrix(G)
		D,max_degree = self.getDegreeMat(np.zeros((len(G.nodes()),len(G.nodes())),dtype=int),nx.degree(G))
		return A,D,max_degree

	def getDegreeMat(self,zero,degree):
		key_list = sorted(degree.keys())
		max_degree = max(degree.values())
		count = 0
		for key in key_list:
			zero[count][count] = degree[key]
			count = count + 1
		return zero,float(1/float(1 + max_degree))

def compare(file1,file2):
	return int(file1.split('_')[0]) - int(file2.split('_')[0])

def main():
	a = Anomaly("/home/abhishek/Downloads/anomaly/datasets/datasets/enron_by_day/")
	a.load_filename()
	a.makeGraph()

if __name__ == '__main__':
	main()