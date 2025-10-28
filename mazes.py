# Utility functions related to mazes

import graphs
import positions
import directions

def createHelperJob(moveDirection):
	def f():
		# quick_print("Spawned helper", moveDirection)
		move(moveDirection)
		# Drones do not need to backtrack at creation because this is the end of their path
		retVal = createInitialGraphHelperParallel(directions.oppositeDirection[moveDirection], False)
		quick_print("12312312331", retVal)
		return retVal
	return f

# This function will return (graph dict<pos, set<pos>>, handlers set<handler>
def createInitialGraphHelperParallel(
	backtrackDirection, # Direction necessary to get to parent state
	shouldBacktrack = True,
	depth = 0
):
	debug = positions.getPos() == (3,6)
	if debug:
		quick_print("DEBUG ACTIVATES")
	graph = graphs.newGraph()
	# quick_print("Starting recursive call", positions.getPos(), backtrackDirection, shouldBacktrack)


	validDirections = []
	for direction in directions.allDirections:
		if direction == backtrackDirection:
			continue
		if can_move(direction):
			validDirections.append(direction)
			graphs.addEdgeBidirectional(
				graph, 
				positions.getPos(), 
				positions.add(positions.getPos(), directions.directionToVector[direction])
			)
	# quick_print("valid directions", validDirections)
	# Keep track of all generated handlers. We need to wait for everyone to complete and merge graphs at the end
	handlers = set()
	if len(validDirections) > 1:
		# quick_print("More than one directions available, trying to fork")
		# Skip the first entry because this drone will always go down the first path
		for direction in validDirections[1:]:
			# quick_print("Handling iteration", i, direction)
			# If a drone is available, send it down this path
			if debug:
				quick_print("DEBUG ACTIVATES 2")
			handler = spawn_drone(createHelperJob(direction))
			# If a drone was not available, then this drone must go down the path and backtrack to finish the route
			if handler == None:
				move(direction)
				# If we are here, we know we need to backtrack
				# This might generate more handlers, 
				g, newHandlers = createInitialGraphHelperParallel(directions.oppositeDirection[direction], True, depth+1)
				if debug:
					quick_print("DEBUG ACTIVATES 7")
				graphs.mergeGraphsMutate(g, graph)
				for newHandler in newHandlers:
					handlers.add(newHandler)
			else:
				handlers.add(handler)
	# If there were any entries, then the first is available, go down it
	if len(validDirections) >= 1:
		if debug:
			quick_print("DEBUG ACTIVATES 3")
		direction = validDirections[0]
		# quick_print("Only one direction valid, recursing", direction)
		move(direction)
		# When a drone recurses itself, it inherits shouldBacktrack because we need to be able to go all the way back if necessary
		# Save the return value in case this drone created more drones down the way
		g, newHandlers = createInitialGraphHelperParallel(directions.oppositeDirection[direction], shouldBacktrack, depth+1)
		if debug:
			quick_print("DEBUG ACTIVATES 8")
		# quick_print("Finished recursive call with", g, newHandlers)
		graphs.mergeGraphsMutate(g, graph)
		for newHandler in newHandlers:
			handlers.add(newHandler)
	if debug:
		quick_print("DEBUG ACTIVATES 4")
	if shouldBacktrack:
		if debug:
			quick_print("DEBUG ACTIVATES 5")
		if backtrackDirection == None:
			while True:	
				pass
		move(backtrackDirection)
	# quick_print("Returning values", graph, handlers)
	if debug:
		quick_print("DEBUG ACTIVATES 6")
		quick_print("DEBUG ACTIVATES RETURNING!!!!!!", depth)
	return graph, handlers
	# Tests says this has almost the same time as just returning everything
	# Attempt to process handlers and graph if possible
	# waitingHandlers = set()
	# processingHandlerQueue = list(handlers)
	# while len(processingHandlerQueue) != 0:
	# 	handler = processingHandlerQueue.pop(0)
	# 	if not has_finished(handler):
	# 		waitingHandlers.add(handler)
	# 	else:
	# 		curGraph, curHandlers = wait_for(handler)
	# 		for curHandler in curHandlers:
	# 			processingHandlerQueue.append(curHandler)
	# 		graphs.mergeGraphsMutate(curGraph, graph)
	# return graph, waitingHandlers


def createInitialGraphHelper(
	graph,
	backtrackDirection, # Direction necessary to get to parent state,
):
	addNeighbors(graph)
	validDirections = set()
	for direction in directions.allDirections:
		if direction == backtrackDirection:
			continue
		if can_move(direction):
			move(direction)
			createInitialGraphHelper(graph, directions.oppositeDirection[direction])
	move(backtrackDirection)

# Checks all sides and adds to graph if it is traversable
# graph is modified by reference
def addNeighbors(graph):
	for direction in directions.allDirections:
		if can_move(direction):
			graphs.addEdge(
				graph, 
				positions.getPos(), 
				positions.add(positions.getPos(), directions.directionToVector[direction])
			)	

# Traverses the entire current maze and returns a graph.
# The graph is two dicts, the adjacency list and it's inverse.
def createInitialGraph(helperFunc):
	# Create initial data structure
	# tuple<dict<pos, set<pos>>, dict<pos, set<pos>>>
	# AKA, an adjacency list dict, and it's inverse
	graph = graphs.newGraph()
	# Add current node
	helperFunc(None, False)
	# graphs.addNode(graph, positions.getPos())
	# addNeighbors(graph)
	# quick_print(graph)
	# for direction in directions.allDirections:
	# 	if can_move(direction):
	# 		move(direction)
	# 		helperFunc(graph, directions.oppositeDirection[direction])
	# quick_print(graph)
	
def createInitialGraphSingle():
	return createInitialGraph(createInitialGraphHelper)

def processResponse(initialProcessorResponse):
	start = get_time()
	totalGraphs = 1
	# quick_print("processing", initialProcessorResponse)
	graph, initialHandlers = initialProcessorResponse
	handlersQueue = list(initialHandlers)
	totalHandlers = len(initialHandlers)
	while len(handlersQueue) != 0:
		# quick_print(handlersQueue)
		handler = handlersQueue.pop(0)
		quick_print("starting wait", handler)
		# if not has_finished(handler):
		# 	quick_print("not finished, requeuing and continue")
		# 	handlersQueue.append(handler)
		# 	continue
		curGraph, curHandlers = wait_for(handler)
		quick_print("wait complete,", handler)
		graphs.mergeGraphsMutate(curGraph, graph)
		totalGraphs += 1
		for subHandler in curHandlers:
			totalHandlers += 1
			handlersQueue.append(subHandler)
	quick_print("elapsed", get_time() - start, totalGraphs, totalHandlers)
	return graph

# Path is a list of positions. The first should be where the drone is, each subsequent are adjacent
def travelPath(path):
	if len(path) < 1:
		return
	for i in range(len(path) - 1):
		dir = positions.directionToPosition(path[i+1], path[i])
		# quick_print("moving", dir)
		move(dir)

# Returns the nubmer of additional paths added
def travelPathWithUpdate(graph, path):
	numFound = 0
	if len(path) < 1:
		return numFound
	for i in range(len(path) - 1):
		for dir in directions.allDirections:
			if can_move(dir):
				if graphs.addEdgeBidirectional(graph, positions.getPos(), positions.add(positions.getPos(), directions.directionToVector[dir])):
					numFound += 1
		dir = positions.directionToPosition(path[i+1], path[i])
		# quick_print("moving", dir)
		move(dir)
	return numFound

def createInitialGraphParallel():
	x = createInitialGraphHelperParallel(None, False)
	# quick_print("FINISHED")
	graph = processResponse(x)
	quick_print("Final graph", graph)
	# keys = 0
	# for key in graph:
	# 	keys += 1
	# quick_print(keys)
	# graphs.renderPositionGraph(graph)
	return graph


def createMaze(size):
	harvest()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, mazePrice(size))	

# Returns true if items were used. False if not (That probably means you're on level 300)
def recreateMaze(size):
	return use_item(Items.Weird_Substance, mazePrice(size))

# Returns the amount of Items.Weird_Substance you have to use to generate a size*size maze
def mazePrice(size):
	return size * 2**(num_unlocked(Unlocks.Mazes) - 1)