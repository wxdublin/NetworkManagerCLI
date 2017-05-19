from util import LOG
import time
import sys
"""
To Simplify the requirements you need to create a Graph and add the routers and edges.
Then create a Requirement in a list.
Once this is done you just need to call Simplifier(Requirement) which will return
a list of the Segments that need to be used for segement routing.
A normal segment is a node segment that needs to be add to the segemnt stack.
A link segment is an adjacency segment that needs to be add to the segemnt stack

"""

class Simplifier(object):
	"""
		Simplifier object,
		represent the network and
		compute minimum label stack of
		requirement

		API functions:
		* add_node
		* add_edge

		* Simplify
	"""
	def __init__(self):
		self.nodes = set()
		self.edges = {}
		self.distances = {}
		self.path = {}

	def Simplify(self,Req):
		"""
			@API
			Compute the minimum LabelsStack
			corresponding to :Req,
			based on view of the network
		"""
		LOG.debug('Simplifying %s' % str(Req))
		Current_req=self.RewriteReq(Req)
		Finalsrc=Req[0]
		Finaldst=Req[-1]
		src=Finalsrc
		dst=Finaldst
		LabelsStack=list()
		finish=True
		while(finish):
			node=self.find_segments(Current_req,src,dst)
			if(node!=False):
				if(node[0]!=Finaldst or node[1] == 'adjacency' ):
					attribute=node[1]
					newDest=node[0]
					dico={'type' : attribute}
					if(attribute=='adjacency'):
						dico['prev']=src
					LabelsStack.append((newDest, dico))
					src=node[0]
					dst=Finaldst
					src_index=Req.index(src)
					dst_index=Req.index(dst)
					Current_req=Req[src_index:dst_index+1]
					Current_req=self.RewriteReq(Current_req)
				else:
					finish=False
				if node[0] == Finaldst :
					finish=False
			else:
				Current_req.pop()
				dst=Current_req[-1][-1]
		LOG.debug('output: %s' % str(LabelsStack))
		return LabelsStack

	def add_node(self, value):
		"""
			@API
		"""
		self.nodes.add(value)

	def add_edge(self, from_node, to_node, distance):
		"""
			@API
		"""
		if(from_node in self.edges):
			self.edges[from_node].append(to_node)
		else:
			self.edges[from_node]=[to_node]
		if(to_node in self.edges):
			self.edges[to_node].append(from_node)
		else:
			self.edges[to_node]=[from_node]

		self.distances[(from_node, to_node)] = distance
		self.distances[(to_node, from_node)] = distance



	# --------------------------------------------
	#    		Lib functions
	# --------------------------------------------
	def DijkstraDag(self, initial):
		nodes = set(self.nodes)

		distance = {}
		previous =  {}

		for node in nodes:
			distance[node] = sys.maxint
			previous[node] = None

		distance[initial] = 0

		while nodes:
			min_node = None
			for node in nodes:
				if node in distance:
					if min_node is None:
						min_node = node
					elif distance[node] < distance[min_node]:
						min_node = node

			if min_node is None:
				break

			nodes.remove(min_node)
			for edge in self.edges[min_node]:
				weight = distance[min_node] + self.distances[(min_node, edge)]
				if edge not in distance or weight < distance[edge]:
					distance[edge] = weight
					previous[edge] = set([min_node])
				elif weight == distance[edge]:
					previous[edge].add(min_node)
		self.path = previous


	def Dic(self):
		edges=set()
		dicEdges={}
		for n in self.path:
			if(self.path[n]):
				for x in self.path[n]:
					edges.add((x,n))
		for In,Out in edges:
			if In not in dicEdges:
				dicEdges[In]=[Out]
			else:
				dicEdges[In].append(Out)
		return dicEdges

	def CleanPath(self,src,dst,mylist,edgesBack,final):
		if(dst!=src):
			if dst in edgesBack:
				for x in edgesBack[dst]:
					if (x,dst) in mylist:
						final.insert(0, (x,dst))
						self.CleanPath(src,x,mylist,edgesBack,final)
		return final

	def BuildPathsHelper(self,src,dst,edges,path):
		if(src!=dst):
			self.DijkstraDag(src)
			if(src in edges):
				for x in edges[src]:
					path.append((src,x))
					self.BuildPathsHelper(x,dst,edges,path)

		return path


	def BuildPaths(self,src,dst):
		edges=self.Dic()
		edgesBack=self.path
		path=list()
		Paths=self.BuildPathsHelper(src,dst,edges,path)
		path=list()
		Paths=self.CleanPath(src,dst,Paths,edgesBack,path)
		return Paths

	def RewriteReq(self,Req):
		NewReq=list()
		for i in range(len(Req)-1):
			NewReq.append((Req[i], Req[i+1]))

		return NewReq

	def degreeToBig(self,dag,Req):
		nodes=set()
		req=set()
		for (x1,x2) in Req:
			req.add(x1)
			req.add(x2)
		for (x1,x2) in dag:
			nodes.add(x1)
			nodes.add(x2)
		degrees=self.Degrees(dag)
		degreeToBig=False;
		node=False
		for n in req:
			if n in nodes:
				if degrees[n]>1:
					degreeToBig=True
					node=n
		return (degreeToBig,node)

	def isIncluded(self,dag,req):

		for r in req:
			if r not in dag:
				return False
		return True

	def Simplifier(self,Req,dest):
		Current_req=self.RewriteReq(Req)
		Finalsrc=Req[0]
		Finaldst=dest
		src=Finalsrc
		dst=Finaldst
		labelend=len(Current_req)
		LabelsStack=list()
		finish=True
		while(finish):
			print('-------')
			print(src)
			print(dst)
			print(Current_req)
			print(labelend)
			node=self.find_segments(Current_req,src,dst)
			time.sleep(1)
			print(node)
			if(node!=False):
				if(node[0]!=Finaldst or node[1] == 'adjacency' ):
					attribute=node[1]
					newDest=node[0]
					dico={'type' : attribute}
					if(attribute=='adjacency'):
						dico['prev']=src
					LabelsStack.append((newDest, dico))
					src=node[0]
					dst=Finaldst
					src_index=Req.index(src)
					dst_index=Req.index(dst)
					Current_req=Req[src_index:dst_index+1]
					Current_req=self.RewriteReq(Current_req)
				else:
					finish=False
			else:
				Current_req.pop()
				print(Current_req)
				dst=Current_req[-1][-1]
		LOG.debug('output: %s' % str(LabelsStack))
		return LabelsStack

	def find_segments(self,Current_req,src,dst):
		self.DijkstraDag(src)
		ShortestPath=self.BuildPaths(src,dst)
		if(self.isIncluded(ShortestPath,Current_req)):
			degree=self.degreeToBig(ShortestPath,Current_req)
			if(not degree[0]):
				return (dst,'normal')
			else:
				Req=list()
				for x in Current_req:
					if x[0] not in Req:
						Req.append(x[0])
					if x[1] not in Req:
						Req.append(x[1])
					if(len(Current_req)==1):
						return (dst, 'adjacency')
				indexreturn=Req.index(degree[1])-1
				return (Req[indexreturn],'normal')

		else:
			if(len(Current_req)==1):
				return (dst, 'adjacency')
			else:
				return False

	def Degrees(self, Path):
		nodes={}
		newPath=set()
		for x in Path:
			newPath.add(x)

		for edge1,edge2 in newPath:
			if edge1 not in nodes:
				nodes[edge1]=0
			if edge2 not in nodes:
				nodes[edge2]=1
			else:
				nodes[edge2]+=1
		return nodes


if __name__ == '__main__':

	routers = [
        'A1',
		'A2',
		'B1',
		'B2',
		'S',
		'D'
    ]


	edges = [
	('A1', 'A2', 1),
	('B1', 'B2', 1),
	('A1', 'B1', 1),
	('A2', 'B2', 3),
	('S','A1',10),
	('D','B2',10)
    ]

	Requirement = ['A1','A2','B2']

	# routers = [
	# 'A','B', 'C', 'D', 'Dest']
	# edges = [
	# ('A', 'B', 1),
	# ('A', 'C', 1),
	# ('D', 'B', 10),
	# ('C', 'D', 1),
	# ('D', 'Dest', 10)
	# ]
	# Requirement = ['A','B','D']

    # build graph
	Network = Simplifier()
	for router in routers :
		Network.add_node(router)

	for edge in edges :
		Network.add_edge(edge[0], edge[1], edge[2])


	test=Network.Simplify(Requirement)
	print(test)

	def mapping_fct(x) :
		if x[1].get('type') == 'normal' :
			return x[0]
		elif x[1].get('type') == 'adjacency' :
			return list((x[1].get('prev') , x[0]))

	Flatten = lambda List: [item for sublist in List for item in sublist]
