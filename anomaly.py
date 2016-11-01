from os import listdir
from os.path import isfile, join
import numpy as np
import networkx as nx
import random as rm
from numpy import matrix
from scipy.linalg import solve
import sys

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
			#print self.file_list

	def loadEdgeVertices(self,index):
		if self.index == self.file_list_size:
			return
		file_name = self.file_list[index]
		graph_file = open(self.file_path + file_name)
		edges = graph_file.read().splitlines()
		self.vertices = range(int(edges[0].split(" ")[0]))
			
		self.edge_lists = map(lambda x:(int(x.split(" ")[0]),int(x.split(" ")[1])),edges[1:])
		#print self.vertices
		#print self.edge_lists

	def makeGraph(self):
		if self.index == self.file_list_size - 1:
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
		ep = min([max1,max2])
		results.append( self.getSimilarityScore(D1,A1,D2,A2,max1,max2,self.vertices)  )
		#print results[-1]
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

	def makeGroups(self, vertex):
		threshold = int(np.sqrt(len(vertex)))
		g = rm.randint(threshold / 2, threshold)
		groups = [list() for x in xrange(g)]

		for elem in vertex:
			groups[rm.randint(0, g - 1)].append(elem)

		return groups

	def getSimilarityScore(self, diag1, adj1, diag2, adj2, epsilon1, epsilon2, vertex):
		groups = self.makeGroups(vertex)
		A1 = matrix(np.identity(len(diag1)) + ((epsilon1 * epsilon1) * diag1) - (epsilon1 * adj1))
		A2 = matrix(np.identity(len(diag2)) + ((epsilon2 * epsilon2) * diag2) - (epsilon2 * adj2))
		rootedDist = 0.0
		N = len(vertex)
		# Commented out matrix creation as maybe not needed to get Similarity Score
		# S1= list()
		# S2= list()
		for group in groups:
			group = set(group)
			groupRow = [1 if index in group else 0 for index in xrange(N)]
			groupCol = matrix(groupRow).T
			_s1 = solve(A1, groupCol)
			_s2 = solve(A2, groupCol)
			rootedDist += sum([pow(np.sqrt(x) - np.sqrt(y), 2) for x, y in zip(_s1, _s2)])
		# S1.append(_s1)
		# S2.append(_s2)
		# S1 = matrix(S1).T
		# S2 = matrix(S2).T
		rootedDist = np.sqrt(rootedDist)
		return 1 / (1 + rootedDist)

def compare(file1,file2):
	return int(file1.split('_')[0]) - int(file2.split('_')[0])

def main():
	global results
	results = list()
	#dirPath = "/home/abhishek/Downloads/anomaly/datasets/datasets/enron_by_day/"
	dirPath = '/home/raunaq/College/GDM/project4/anomaly/datasets/datasets/enron_by_day/'
	if len(sys.argv)>1:
		dirPath = str(sys.argv[1])
	a = Anomaly(dirPath)
	a.load_filename()
	while a.makeGraph():
		pass

if __name__ == '__main__':
	main()
