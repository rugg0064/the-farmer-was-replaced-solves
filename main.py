import f2
import lists
import newSerpentine
import boundaries
import positionsFast
import pumpkins
import sets
import positions
import sunflowers
import graphs
import directions
import mazes
import serpentine
import snakePath
import paths

#set_world_size(6)
#set_execution_speed(6)

clear()

def makeJob(bounds):
	plan = newSerpentine.makeSerpentinePlan(bounds, newSerpentine.SERPENTINE_MODE_VERTICAL)
	action = pumpkins.getPumpkinAction(bounds)
	i = 0
	def job():
		global i
		while True:
			set = action()
			quick_print(len(set), boundaries.getArea(bounds) * 0.75)
			if len(set) < boundaries.getArea(bounds) * 0.50:
				plan()
			else:
				diff = sets.diff(set, boundaries.getAllPositions(bounds))
				if i >= len(diff):
					i = 0
				positions.gotoPos(list(diff)[i])
				i += 1
				#plan()
	return job

def farmPumpkins():
	while True:
		spawn_drone(makeJob(boundaries.fromBottomLeft((7,0), (6, 6))))
		spawn_drone(makeJob(boundaries.fromBottomLeft((14,0), (6, 6))))

		spawn_drone(makeJob(boundaries.fromBottomLeft((0,7), (6, 6))))
		spawn_drone(makeJob(boundaries.fromBottomLeft((7,7), (6, 6))))
		spawn_drone(makeJob(boundaries.fromBottomLeft((14,7), (6, 6))))

		spawn_drone(sunflowers.makeSunflowersJob((boundaries.fromBottomLeft((0,14), (6, 6)))))

		# spawn_drone(makeJob(boundaries.fromBottomLeft((0,14), (6, 6))))
		spawn_drone(makeJob(boundaries.fromBottomLeft((7,16), (6, 6))))
		# spawn_drone(makeJob(boundaries.fromBottomLeft((14,14), (6, 6))))

		makeJob(boundaries.fromBottomLeft((0,0), (6, 6)))()
		#sunflowers.makeSunflowersJob(boundaries.fromBottomLeft((0,0), (6, 6)))()

totalTime = 0

def droneTesting():
	def makeDroneJob(id, depth):
		def droneJob():
			positions.gotoPos((random() * 10 // 1, random() * 10 // 1))
			handlers = []
			if depth < 10:
				spawned = 0
				while spawned < 4:
					handler = spawn_drone(makeDroneJob(random(), depth+1))
					if handler != None:
						handlers.append(handler)
						spawned += 1
			return id, depth, handlers
		return droneJob
	handlers = []
	handlers.append(spawn_drone(makeDroneJob(1, 1)))
	while len(handlers) > 0:
		quick_print(handlers)
		handler = handlers.pop()
		resp = wait_for(handler)
		for subHandler in resp[2]:
			handlers.append(subHandler)
		#quick_print(resp)

def carrots():
	def makeCarrotJob():
		def f():
			serpentine.doForAll(newSerpentine.makeSerpentinePlan(boundaries.getWorldBounds(), newSerpentine.SERPENTINE_MODE_VERTICAL), till, boundaries.getWorldBounds())
			while True:
				move(directions.allDirections[random() * 4 // 1])
				if can_harvest():
					harvest()
				plant(Entities.Carrot)
		return f
	spawn_drone(makeCarrotJob())
	spawn_drone(makeCarrotJob())
	spawn_drone(makeCarrotJob())
	spawn_drone(makeCarrotJob())
	spawn_drone(makeCarrotJob())
	spawn_drone(makeCarrotJob())
	spawn_drone(makeCarrotJob())

def doMazes():
	#g = graphs.newGraph()
	#graphs.addEdgeBidirectional(g, "a", "b")
	#quick_print(g)
	# set_execution_speed(5)
	#change_hat(Hats.Brown_Hat)
	#positions.gotoPos((3, 3))

	mazeSize = 22
	numDrones = 16 # max_drones()

	set_world_size(mazeSize)
	mazes.createMaze(mazeSize)
	graph = mazes.createInitialGraphParallel()
	quick_print("Done with graphing")
	
	def initSetup(graph):
		quick_print("Initializing on graph", graph)
		droneHomes = [(random() * get_world_size() // 1, random() * get_world_size() // 1)]
		
		maxBfs = graphs.breadthFirstSearchAllCosts(graph, droneHomes[0]) # Dict<position, cost>
		quick_print("got bfs", maxBfs)
		# Have to make a copy for the singleDroneCosts
		copy = {}
		for key in maxBfs:
			copy[key] = maxBfs[key]
		singleDroneCosts = {0: copy} # dict<droneId, dict<position, cost>>
		def getMaxBfs():
			maxVertex = None
			maxCost = None
			for vertex in maxBfs:
				cost = maxBfs[vertex]
				if maxVertex == None:
					maxVertex = vertex
					maxCost = cost
				elif cost > maxCost:
					maxVertex = vertex
					maxCost = cost
			return maxVertex
		# Modifies bfs1
		# Goes through each node of bfs1 and sets it to the min(this, that)
		# IE its the shortest cost to any node
		def mergeBfs(bfs1, bfs2):
			for key in bfs1:
				bfs1[key] = min(bfs1[key], bfs2[key])
		for id in range(1, numDrones):
			vertex = getMaxBfs()
			droneHomes.append(vertex)
			droneCosts = graphs.breadthFirstSearchAllCosts(graph, vertex)
			mergeBfs(maxBfs, droneCosts)
			singleDroneCosts[id] = droneCosts
		# quick_print("Chose homes", droneHomes)
		# quick_print("maxBfs", maxBfs)
		whoGoesWhere = {}
		for key in maxBfs:
			closestDroneId = None
			closestDroneCost = None
			for droneId in range(numDrones):
				cost = singleDroneCosts[droneId][key]
				if closestDroneId == None:
					closestDroneId = droneId
					closestDroneCost = cost
				if cost < closestDroneCost:
					closestDroneId = droneId
					closestDroneCost = cost
			whoGoesWhere[key] = closestDroneId
		

		def renderPosNumber(graph):
			topLeft = (999999, -99999)
			bottomRight = (-999999, 999999)
			for position in graph:
				topLeft = (min(positions.getX(topLeft), positions.getX(position)), max(positions.getY(topLeft), positions.getY(position)))
				bottomRight = (max(positions.getX(bottomRight), positions.getX(position)), min(positions.getY(bottomRight), positions.getY(position)))
			for y in range(positions.getY(topLeft), positions.getY(bottomRight) - 1, -1):
				outString = ""
				for x in range(positions.getX(topLeft), positions.getX(bottomRight) + 1):
					outString += " " + str(graph[(x,y)]) + " "
				quick_print(outString)
			quick_print("")
		topLeft = (999999, -99999)
		bottomRight = (-999999, 999999)
		for position in whoGoesWhere:
			topLeft = (min(positions.getX(topLeft), positions.getX(position)), max(positions.getY(topLeft), positions.getY(position)))
			bottomRight = (max(positions.getX(bottomRight), positions.getX(position)), min(positions.getY(bottomRight), positions.getY(position)))
		# whoGoesWhere rendering
		def renderWhoGoes():
			quick_print("WHO GOES WHERE	")
			for y in range(positions.getY(topLeft), positions.getY(bottomRight) - 1, -1):
				outString = ""
				for x in range(positions.getX(topLeft), positions.getX(bottomRight) + 1):
					found = False
					for droneId in range(numDrones):
						if droneHomes[droneId] == (x,y):
							found = True
							outString += "[" + str(droneId) +"]"
					if not found:
						outString += " " + str(whoGoesWhere[(x,y)]) + " "
				quick_print(outString)
				quick_print("")
		# renderWhoGoes()
		#quick_print("Computed who goes where", whoGoesWhere)

		# maxBfs rendering
		# quick_print("MAX BFS")
		# renderPosNumber(maxBfs)
		# for costTableKey in singleDroneCosts:
		# 	quick_print("sdc", costTableKey)
		# 	# quick_print(costTableKey)
		# 	renderPosNumber(singleDroneCosts[costTableKey])

		return droneHomes, whoGoesWhere, closestDroneCost

	def spawnChildren(graph, droneHomes, whoGoesWhere, closestDroneCost):
		handlers = []
		for i in range(1, numDrones):
			quick_print("spawning", i)
			handlers.append(spawn_drone(droneJob(i, False, graph, droneHomes, whoGoesWhere, closestDroneCost)))
		return handlers

	def droneJob(id, isMaster, initGraph, initDroneHomes, initWhoGoesWhere, initClosestDroneCost):
		def f():
			handlers = []
			graph = initGraph
			droneHomes = initDroneHomes
			whoGoesWhere = initWhoGoesWhere
			closestDroneCost = initClosestDroneCost

			hasFoundAllDrones = False
			numNewEdges = 0
			home = None
			if isMaster:
				pass
			else:	
				home = droneHomes[id]

			def returnHome():
				pathHome = graphs.breadthFirstSearch(graph, positions.getPos(), home)
				#quick_print("Going home", positions.getPos(), home, pathHome)
				mazes.travelPath(pathHome)
			while True:
				if isMaster:
					if num_drones() != numDrones:
						quick_print("Master detected dead slave. Waiting for all to die")
						while num_drones() != 1:
							pass
						quick_print("hhh", handlers)
						start = get_time()
						for handler in handlers:
							resp = wait_for(handler)
							# quick_print("123123123", resp)
							if resp == None:
								quick_print("None response suggests maze was completed")
								if get_entity_type() == Entities.Hedge:
									quick_print("ERROR ERROR ERROR. Got None but still in a hedge.")
								else:
									quick_print("Finished program", get_tick_count(), get_time())
									return
							graphs.mergeGraphsMutate(resp, graph)
						global totalTime
						totalTime += get_time() - start
						quick_print("totalTime", totalTime)
						# graphs.renderPositionGraph(graph)
						droneHomes, whoGoesWhere, closestDroneCost = initSetup(graph)
						home = droneHomes[id]
						handlers = spawnChildren(graph, droneHomes, whoGoesWhere, closestDroneCost)
				else: # Is slave
					if not hasFoundAllDrones:
						hasFoundAllDrones = num_drones() == numDrones
					else:
						if num_drones() != numDrones:
							quick_print("Found mismatch in drones. Killing self to restart")
							return graph
						if numNewEdges > 999:
							quick_print("Found new edges, killing")
							# Found enough edges to force reset the system
							return graph
				if not positions.areEqual(home, positions.getPos()):
					returnHome()
				def handleIsClosest():
					global numNewEdges
					treasure = measure()
					if treasure == None:
						quick_print("Treasure was None. Maze is over. Killing.")	
						return None
					if whoGoesWhere[treasure] == id:
						quick_print("I AM THE CLOSEST!", id, closestDroneCost, measure(), positions.getPos())
						path = graphs.breadthFirstSearch(graph, positions.getPos(), measure())
						quick_print("path", path)
						numNewEdges += mazes.travelPathWithUpdate(graph, path)
						if not mazes.recreateMaze(mazeSize):
							harvest()
							return None
						return True
					return False
				run = True
				while run:
					run = handleIsClosest()
					if not isMaster:
						if run == None:
							return None
		return f

	# droneHomes, whoGoesWhere, closestDroneCost = initSetup(graph)
	# handlers = spawnChildren(graph, droneHomes, whoGoesWhere, closestDroneCost)
	droneJob(0, True, graph, None, None, None)()
	quick_print("gold", num_items(Items.Gold))
	# for i in range(20):
	# 	quick_print("Running execution", i)
	# 	path = graphs.breadthFirstSearch(g, positions.getPos(), measure())
	# 	quick_print("Done with searching")
	# 	quick_print(path)
	# 	mazes.travelPath(path)
	# 	if i == 19:
	# 		quick_print("HARVESTING", i)
	# 		harvest()
	# 	else:
	# 		mazes.recreateMaze(mazeSize)

def harvestingTests():
	def makeJob(bounds):
		def f():
			path = snakePath.makeSnakePath(bounds, boundaries.getBottomLeft(bounds), East)
			pathDirDict = paths.pathToDirDict(path, True)
			positions.gotoPos(path[0])
			quick_print(pathDirDict)
			while True:
				move(pathDirDict[positions.getPos()])
				if get_ground_type() == Grounds.Grassland:
					till()
					plant(Entities.Carrot)
				if can_harvest():
					harvest()
					plant(Entities.Carrot)
		return f	
	
	def makeJobWheat(bounds):
		def f():
			path = snakePath.makeSnakePath(bounds, boundaries.getBottomLeft(bounds), East)
			pathDirDict = paths.pathToDirDict(path, True)
			positions.gotoPos(path[0])
			quick_print(pathDirDict)
			while True:
				move(pathDirDict[positions.getPos()])
				if can_harvest():
					harvest()
					plant(Entities.Grass)
		return f	

	quick_print("11111!23")
	# path = snakePath.makeSnakePath(, , East)
	# pathDirDict = paths.pathToDirDict(path, True)
	spawn_drone(sunflowers.makeSunflowersJob((boundaries.fromBottomLeft((0,16), (22, 6)))))
	# for x in range(0, 32, 4):
	# 	for y in range(0, 32, 4):
	# 		if x == 0 and y == 0:
	# 			continue
	# 		quick_print(x, y)
	# 		spawn_drone(makeJob(boundaries.fromBottomLeft((x, y), (5,5))))


	# spawn_drone(makeJob(boundaries.fromBottomLeft((6, 0), (6,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((12, 0), (6,6))))

	# spawn_drone(makeJob(boundaries.fromBottomLeft((0, 6), (6,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((6, 6), (6,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((12, 6), (6,6))))

	# spawn_drone(makeJob(boundaries.fromBottomLeft((0, 12), (6,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((6, 12), (6,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((12, 12), (6,6))))

	# spawn_drone(makeJob(boundaries.fromBottomLeft((0, 18), (6,4))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((6, 18), (6,4))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((12, 18), (6,4))))

	# spawn_drone(makeJob(boundaries.fromBottomLeft((18, 0), (4,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((18, 6), (4,6))))
	# spawn_drone(makeJob(boundaries.fromBottomLeft((18, 12), (4,6))))


	# spawn_drone(makeJob(boundaries.fromBottomLeft((18, 18), (4,4))))


	spawn_drone(makeJobWheat(boundaries.fromBottomLeft((0, 8), (4,4))))
	spawn_drone(makeJobWheat(boundaries.fromBottomLeft((4, 8), (4,4))))
	spawn_drone(makeJobWheat(boundaries.fromBottomLeft((0, 12), (4,4))))
	spawn_drone(makeJobWheat(boundaries.fromBottomLeft((4, 12), (4,4))))
	spawn_drone(makeJob(boundaries.fromBottomLeft((10, 8), (12,8))))

	spawn_drone(makeJob(boundaries.fromBottomLeft((0, 0), (10, 8))))
	makeJob(boundaries.fromBottomLeft((10, 0), (12,8)))()

def main():
	#carrots()
	#doMazes()

	# mazeSize = 10	
	# numDrones = 16 # max_drones()
	# set_world_size(mazeSize)
	# mazes.createMaze(mazeSize)
	# graph = mazes.createInitialGraphParallel()
	# quick_print(graph)
	# quick_print(positions.getPos())
	# quick_print(str(get_time()) + " seconds")
	# graphs.renderPositionGraph(graph)

	# x = [4,1,2,3,5,12,3,5,12,5]
	# print(x)
	# qsort(x)
	# print(x)
	# cpy = [4,1,2,3,5,12,3,5,12,5]
	# cpy.sort()
	# print(cpy)

	numDrones = 16

	def j(bounds):
		def f():
			sunflowers.multiSunflower(bounds, numDrones)		 
		return f

	spawn_drone(j(boundaries.fromBottomLeft((6, 0), (6,6))))
	spawn_drone(j(boundaries.fromBottomLeft((12, 0), (6,6))))

	spawn_drone(j(boundaries.fromBottomLeft((0, 6), (6,6))))
	spawn_drone(j(boundaries.fromBottomLeft((6, 6), (6,6))))
	spawn_drone(j(boundaries.fromBottomLeft((12, 6), (6,6))))

	spawn_drone(j(boundaries.fromBottomLeft((0, 12), (6,6))))
	spawn_drone(j(boundaries.fromBottomLeft((6, 12), (6,6))))
	spawn_drone(j(boundaries.fromBottomLeft((12, 12), (6,6))))

	spawn_drone(j(boundaries.fromBottomLeft((0, 18), (6,4))))
	spawn_drone(j(boundaries.fromBottomLeft((6, 18), (6,4))))
	spawn_drone(j(boundaries.fromBottomLeft((12, 18), (6,4))))

	spawn_drone(j(boundaries.fromBottomLeft((18, 0), (4,6))))
	spawn_drone(j(boundaries.fromBottomLeft((18, 6), (4,6))))
	spawn_drone(j(boundaries.fromBottomLeft((18, 12), (4,6))))


	spawn_drone(j(boundaries.fromBottomLeft((18, 18), (4,4))))

	sunflowers.multiSunflower(boundaries.fromBottomLeft((0, 0), (6,6)), numDrones)




if __name__ == '__main__':
	main()