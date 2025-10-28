# Graphs

import positions
import lists

# A graph is just a dictionary adjacency list. For now there is no inverse, it is directed by default.

def newGraph():
	return {}

def addVertex(graph, vertex):
	if vertex not in graph:
		graph[vertex] = set()

# Creates a directional edge from a to b
# Creates vertices if they don't exist
# Returns true if an edge was created
def addEdge(graph, a, b):
	addVertex(graph, a)
	addVertex(graph, b)
	sa = graph[a]
	if b not in sa:
		sa.add(b)
		return True
	return False

# Creates an edge from a to b and b to a 
# Returns true if at least one edge was created
def addEdgeBidirectional(graph, a, b):
	aSucceed = addEdge(graph, a, b)
	bSucceed = addEdge(graph, b, a)
	return aSucceed or bSucceed

def getConnectedVertices(graph, vertex):
	if vertex in graph:
		return graph[vertex]
	return set()

def doesVertexExist(graph, vertex):
	return vertex in graph

def getVertices(graph):
	vertices = set()
	for key in graph:
		vertices.add(key)
	return vertices

# Places all entries from sourceGraph into destinationGraph. Modified dst reference. No copy
def mergeGraphsMutate(sourceGraph, destinationGraph):
	for sourceVertex in getVertices(sourceGraph):
		for destinationVertex in getConnectedVertices(sourceGraph, sourceVertex):
			addEdge(destinationGraph, sourceVertex, destinationVertex)

# Returns a new graph that combines all vertices and edges from graphs g1 and g2
def mergeGraphs(g1, g2):
	graph = newGraph()
	for src in getVertices(g1):
		for dst in getConnectedVertices(g1, src):
			addEdge(graph, src, dst)
	for src in getVertices(g2):
		for dst in getConnectedVertices(g2, src):
			addEdge(graph, src, dst)
	return graph

def mergeAllGraphs(graphList):
	merge = newGraph()
	for graph in graphList:
		merge = mergeGraphs(merge, graph)
	return merge


# graph must be a graph of positions
def renderPositionGraph(graph):
	rendering = {
		# NESW
		0: " ",  #0b0000
		8: "N",  #0b1000
		4: "E",  #0b0100
		2: "S",  #0b0010
		1: "W",  #0b0001

		12: "└",  #0b1100
		6: "┌",  #0b0110
		3: "┐",  #0b0011
		9: "┘",  #0b1001
		10: "│",  #0b1010
		5: "─",  #0b0101

		14: "├", #0b1110
		7: "┬", #0b0111
		11: "┤", #0b1011
		13: "┴", #0b1101

		15: "┼"   #0b1111
	}
	topLeft = (999999, -99999)
	bottomRight = (-999999, 999999)
	for vertex in graph:
		topLeft = (min(positions.getX(topLeft), positions.getX(vertex)), max(positions.getY(topLeft), positions.getY(vertex)))
		bottomRight = (max(positions.getX(bottomRight), positions.getX(vertex)), min(positions.getY(bottomRight), positions.getY(vertex)))
	for y in range(positions.getY(topLeft), positions.getY(bottomRight) - 1, -1):
		str = ""
		for x in range(positions.getX(topLeft), positions.getX(bottomRight) + 1):
			# quick_print("handling", (x, y))
			vertices = getConnectedVertices(graph, (x, y))
			renderValue = 0 #0b0000
			for vertex in vertices:
				if positions.getX(vertex) < x:
					renderValue = renderValue + 1 #0b0001
				if positions.getX(vertex) > x:
					renderValue = renderValue + 4 #0b0100
				if positions.getY(vertex) < y:
					renderValue = renderValue + 2 #0b0010
				if positions.getY(vertex) > y:
					renderValue = renderValue + 8 #0b1000
			str += rendering[renderValue]
		quick_print(str)


def breadthFirstSearch(graph, start, end):
	if start not in graph:
		return None
	if end not in graph:
		return None
	exploredVertices = set([start])
	# This is a full list of paths
	paths = [[start]]
	while paths:
		curPath = paths.pop(0)
		last = lists.last(curPath)
		exploredVertices.add(last)
		if last == end:
			return curPath
		for vertex in getConnectedVertices(graph, last):
			if vertex in exploredVertices:
				continue
			copy = lists.copy(curPath)
			copy.append(vertex)
			paths.append(copy)
	return None

def breadthFirstSearchCost(graph, start, end):
	#quick_print("Getting cost for", start, end)
	path = breadthFirstSearch(graph, start, end)
	#quick_print("Got cost", path)
	cost = len(path) - 1
	return cost

# Returns a dict of each destination and it's cost
# Destinations is a set<destination> aka set<tuple<position, any>>
# Returns dict<destination, cost number>>
def breadthFirstSearchCosts(graph, start, destinations):
	# Todo: Modify the bfs so it stops once all destinations are found
	# Todo: Swap this with a single bfs execution that only tracks costs, not paths, and finds every destination in one sweep
	#quick_print("Getting all costs for", start, destinations)
	retVal = {}
	for destination in destinations:
		destinationPosition = destination[0]
		cost = breadthFirstSearchCost(graph, start, destinationPosition)
		retVal[destination] = cost
	return retVal

# Returns a dict<vertex, cost> which is the cost to get from startVertex to vertex
def breadthFirstSearchAllCosts(graph, startVertex):
	quick_print("bfsCosts on", startVertex, graph)
	if startVertex not in graph:
		quick_print("startVertex not found")
		return None
	costs = {}
	verticesToExplore = [(startVertex, 0)] # Queue < Tuple < Vertex, Cost > >

	while verticesToExplore:
		curVertex, curPrice = verticesToExplore.pop(0)
		costs[curVertex] = curPrice
		for vertex in getConnectedVertices(graph, curVertex):
			if vertex in costs:
				continue
			verticesToExplore.append((vertex, curPrice + 1))
	return costs
