from os import listdir
from os.path import isfile, join
import numpy as np
import networkx as nx
import random as rm
from numpy import matrix
from scipy.sparse.linalg import spsolve
import sys
from scipy.sparse import lil_matrix,identity,csr_matrix

class Anomaly:
	file_path = None
	file_list = None
	edge_lists = None
	vertices = None
	index = 0
	file_list_size = None
	g=None

	def __init__(self,file_path):
		self.file_path = file_path

	def load_filename(self):
		"""
		Takes files from the directory and puts them in sorted order as per number
		"""
		self.file_list = [f for f in listdir(self.file_path) if isfile(join(self.file_path, f))]
		self.file_list = sorted(self.file_list,cmp=compare)
		self.file_list_size = len(self.file_list)


	def loadEdgeVertices(self,index):
		"""
		:param index: Index of graphfile being considered
		Function sets vertices and edge values of particular graphfile
		"""
		if self.index == self.file_list_size:
			return
		file_name = self.file_list[index]
		graph_file = open(self.file_path + file_name)
		edges = graph_file.read().splitlines()
		self.vertices = range(int(edges[0].split(" ")[0]))
		self.edge_lists = map(lambda x:(int(x.split(" ")[0]),int(x.split(" ")[1])),edges[1:])

	def makeGraph(self):
		"""
		Computes similarity of next two graph files
		:return: True if more files present to find similarity, returns False
		"""
		if self.index == self.file_list_size - 1:
			return False
		"""
		Loading data and creating first graph of Pair
		"""
		self.loadEdgeVertices(self.index)
		G1 = nx.Graph()
		G1.add_nodes_from(self.vertices)
		G1.add_edges_from(self.edge_lists)
		"""
		Loading data and creating second graph of Pair
		"""
		self.loadEdgeVertices(self.index + 1)
		G2 = nx.Graph()
		G2.add_nodes_from(self.vertices)
		G2.add_edges_from(self.edge_lists)
		"""
		If G has not been calculated, sets its value
		"""
		if self.index==0:
			self.setG(len(self.vertices))
		self.index = self.index + 1
		A1,D1,max1 = self.makeDiagonal(G1)
		A2,D2,max2 = self.makeDiagonal(G2)
		results.append( self.getSimilarityScore(D1,A1,D2,A2,max1,max2,self.vertices)  )
		#print results[-1]
		return True

	def makeDiagonal(self,G):
		"""
		:param G: Graph object of networkx
		:return: Adjacency Matrix (A), Degree Matrix(D), max_degree - epsilon value
		"""
		A = nx.adjacency_matrix(G)
		D,max_degree = self.getDegreeMat(lil_matrix((len(G.nodes()),len(G.nodes())),dtype=int),nx.degree(G))
		return A,D,max_degree

	def getDegreeMat(self,zero,degree):
		key_list = sorted(degree.keys())
		max_degree = max(degree.values())
		#Creating degree matrix and setting values of diagonal
		zero.setdiag(key_list)
		return zero,float(1/float(1 + max_degree))

	def setG(self,length):
		"""
		:param length: number of vertices
		sets value of G between square-root(length)/2 --->  square-root(length)  [since G<<length]
		"""
		threshold = int(np.sqrt(length))
		self.g = rm.randint(threshold / 2, threshold)

	def makeGroups(self, vertex):
		"""
		:param vertex: list of vertices
		:return: list of groups
		"""
		groups = [list() for x in xrange(self.g)]
		for elem in vertex:
			groups[rm.randint(0, self.g - 1)].append(elem)
		return groups

	def getSimilarityScore(self, diag1, adj1, diag2, adj2, epsilon1, epsilon2, vertex):
		"""
		Function computes the values by linearly solving the Ax=B Matrix equation using spsolve
		Calculates rootedDist summation in the loop to avoid creation of additional matrix
		:return: Similarity score of two graphs
		"""
		groups = self.makeGroups(vertex)
		#Computes left hand static side of equation Ax=B
		A1 = identity(diag1.shape[0]) + ((epsilon1 * epsilon1) * diag1) - (epsilon1 * adj1)
		A2 = identity(diag2.shape[0]) + ((epsilon2 * epsilon2) * diag2) - (epsilon2 * adj2)
		rootedDist = 0.0
		N = len(vertex)

		for group in groups:
			#Generating s0k base RHS of equation
			group = set(group)
			groupRow = [1 if index in group else 0 for index in xrange(N)]
			groupCol = csr_matrix(groupRow).T
			_s1 = spsolve(A1, groupCol)
			_s2 = spsolve(A2, groupCol)
			#summation of  (sqrt(Xi) - sqrt(Yi))^2
			rootedDist += sum([pow(np.sqrt(x) - np.sqrt(y), 2) for x, y in zip(_s1, _s2)])

		rootedDist = np.sqrt(rootedDist)
		return 1 / (1 + rootedDist)

def compare(file1,file2):
	return int(file1.split('_')[0]) - int(file2.split('_')[0])

def main():
	#containing results of all graph similarities
	global results
	results = list()

	if len(sys.argv)>1:
		dirPath = str(sys.argv[1])
	else:
		print 'Please enter directory path as argument with ending /'
		exit()

	a = Anomaly(dirPath)
	#Loads list of files in filename
	a.load_filename()
	#keep executing till more adjacent pairs not present
	while a.makeGraph():
		pass

	fname = dirPath.split("/")[-2]
	fname = fname + "_time_series.txt"
	fp = open(fname, 'w+')
	#print results
	#write results to the file
	for elem in results:
		fp.write(str(elem)+'\n')
	fp.close()

if __name__ == '__main__':
	main()
