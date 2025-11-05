import paths
import positionsFast
import snakePath
import utils
import serpentine
import lists
import positions
import boundaries
import f2
import newSerpentine

SUNFLOWER_MAX_TIME = 8.4 

def positionPetalsComparator(a, b):
	return lists.numAscend(a[0], b[0])

def makeSunflowersJob(bounds):
	def f():
		doSunflowers(bounds)
	return f

def doSunflowers(bounds):
	positions.gotoPos(boundaries.getMin(bounds))
	# (pedals, position)
	positionPetals = []
	# First plant everything and get data in good state
	def plantJob():
		plant(Entities.Sunflower)
		lists.sortedInsert(positionPetals, (measure(), positions.getPos()), positionPetalsComparator)
	# Plants on bounds
	serpentine.doForAll(newSerpentine.makeSerpentinePlan(bounds, newSerpentine.SERPENTINE_MODE_VERTICAL),
					 f2.combineActions(utils.ensureTilled, plantJob), bounds)
	do_a_flip()
	# Harvesting loop
		
	def gotoWaitHarvest(pos):
		positions.gotoPos(best[1])
		while not can_harvest():
			do_a_flip()
		harvest()
	
	while True:
		replant = []
		while len(positionPetals) >= 10:
			# Go to best
			best = positionPetals.pop()
			gotoWaitHarvest(best[1])
			replant.append(best[1])
		# serpentine.doForAll(newSerpentine.makeSerpentinePlan(bounds, newSerpentine.SERPENTINE_MODE_VERTICAL),
		# 			 f2.combineActions(utils.ensureTilled, plantJob), bounds)
		for pos in replant:
			positions.gotoPos(pos)
			plantJob()

def singleSunflower(bounds):
	path = snakePath.makeSnakePath(bounds, boundaries.getBottomLeft(bounds), East)
	positions.gotoPos(path[0])
	pathDirs = paths.pathToDirections(path, True)
	pathPosDirs = paths.pathToDirDict(path, True)
	i = 0
	harvestPath = []
	# (pedals, position)
	# Dict<measure(), array<position>>
	positionPetals = {}
	def resetPositionPetals():
		global positionPetals
		for i in range(7, 15+1): # Initialize [7,15]
			positionPetals[i] = set()
	def measureRecord():
		positionPetals[measure()].add(positions.getPos())
	def doPlantAndTill():
		for i in range(len(path)):
			till()
			plant(Entities.Sunflower)
			measureRecord()
			move(pathPosDirs[positions.getPos()])
	def doPlant():
		for i in range(len(path)):
			plant(Entities.Sunflower)
			measureRecord()
			move(pathPosDirs[positions.getPos()])
	def createPath():
		# Creates a greedy path, going from each flower level descending. Picks the closest flower from the last position
		global harvestPaths
		harvestPaths = [positions.getPos()]
		# Will remove first entry at the end to make it only flowers
		for i in range(15, 6 , -1): #[15, 7] Iterate through each measure of flowers to ensure we get the bonus
			entries = positionPetals[i] # Reference to the active collection of flowers
			thisLevelPath = []
			for _ in range(0, len(entries)): # Now actual sort sequence. For each entry.. Get the closest
				closestPos = None
				shortestDistance = 9999999
				for pos in entries:
					distance = positionsFast.manhattanDistance(pos, lists.last(harvestPaths))
					if distance < shortestDistance:
						closestPos = pos
						shortestDistance = distance
				# Found closest entry. Add it to path and remove for next iteration
				harvestPaths.append(closestPos)
				thisLevelPath.append(closestPos)
				entries.remove(closestPos)	
			# quick_print(thisLevelPath)
		harvestPaths.pop(0) # Remove first entry
		return harvestPaths
	def harvestAll():
		for i in range(0, len(harvestPath)-11): # Equivalent to [0, allButLast9]
			pos = harvestPath[i]
			positions.gotoPos(pos)
			while not can_harvest():
				pass
			harvest()
	# def doPlanting():
	# 	for i in range(len(path)):
	# 		pathPosDirs
	resetPositionPetals()
	doPlantAndTill()
	createPath()
	harvestAll()
	resetPositionPetals()
	while True:
		doPlant()
		createPath()
		harvestAll()
		resetPositionPetals()

def multiSunflower(bounds, numDrones):
	totalTiles = boundaries.getArea(bounds)
	path = snakePath.makeSnakePath(bounds, boundaries.getBottomLeft(bounds), East)
	positions.gotoPos(path[0])
	pathDirs = paths.pathToDirections(path, True)
	pathPosDirs = paths.pathToDirDict(path, True)
	startWoodCount = num_items(Items.Wood)
	plantCarrotWoodCost = get_cost(Entities.Carrot)[Items.Wood]
	stages = ["Plant", 0, 1, 2, 3, 4, 5, 6, 7, 8] # Planting stage and indices of the harvestPaths
	def getStage():
		# Planting a carrot costs plantCarrotWoodCost
		# We can check how many we have since we started
		# Therefore, we can communicate.
		# It takes numDrones plants in order to proceed to the next level
		# Therefore, numPlantedSoFar // numDrones*plantCarrotWoodCost should give us the stage we are on
		# numPlantedSoFar is just start - num_items
		# Mod by length and return as string
		return stages[((startWoodCount - num_items(Items.Wood)) // (numDrones*plantCarrotWoodCost)) % len(stages)]

	i = 0
	harvestPaths = []
	# (pedals, position)
	# Dict<measure(), array<position>>
	positionPetals = {}
	def resetPositionPetals():
		global positionPetals
		for i in range(7, 15+1): # Initialize [7,15]
			positionPetals[i] = set()
	def measureRecord():
		positionPetals[measure()].add(positions.getPos())
	def tillAll():
		for i in range(len(path)):
			till()
			move(pathPosDirs[positions.getPos()])
	def doPlantAndTill():
		for i in range(len(path)):
			till()
			plant(Entities.Sunflower)
			measureRecord()
			move(pathPosDirs[positions.getPos()])
		quick_print(positionPetals)
	def doPlant(): # Plants all but the last square
		for i in range(len(path) - 1):
			plant(Entities.Sunflower)
			measureRecord()
			move(pathPosDirs[positions.getPos()])
	def createPath():
		# Creates a series of greedy paths, one for each flower level descending.
		# In series, they form a greedy path starting with the current position and always going to the next flower closest to the last.
		global harvestPaths
		lastPos = positions.getPos()
		harvestPaths = []
		for i in range(7, 15+1): # [7,15]
			harvestPaths.append([])
		# Will remove first entry at the end to make it only flowers
		levelIndex = 0
		for i in range(15, 6 , -1): #[15, 7] Iterate through each measure of flowers to ensure we get the bonus
			entries = positionPetals[i] # Reference to the active collection of flowers
			quick_print(i, "posp", entries)
			for _ in range(0, len(entries)): # Now actual sort sequence. For each entry.. Get the closest
				closestPos = None
				shortestDistance = 9999999
				for pos in entries:
					distance = positionsFast.manhattanDistance(pos, lastPos)
					if distance < shortestDistance:
						closestPos = pos
						shortestDistance = distance
				# Found closest entry. Add it to path and remove for next iteration
				quick_print(i, levelIndex, closestPos, harvestPaths[levelIndex])
				harvestPaths[levelIndex].append(closestPos)
				lastPos = closestPos
				entries.remove(closestPos)	
			# quick_print(thisLevelPath)
			quick_print("finish lvl with", harvestPaths[levelIndex])
			levelIndex += 1
	def harvestAll():
		numberToHarvest = totalTiles - 10
		for index in range(len(harvestPaths)):
			while getStage() != index:
				quick_print("On stage", getStage(), "waiting for", index)
				continue
			levelPath = harvestPaths[index]
			for pos in levelPath:
				positions.gotoPos(pos)
				while not can_harvest():
					pass
				harvest()
				numberToHarvest += 1
			plant(Entities.Carrot)
			harvest()
	resetPositionPetals()
	tillAll()
	while True:
		while getStage() != "Plant":
			quick_print("On stage", getStage(), "waiting for", "Plant")
		doPlant()
		plant(Entities.Carrot)
		harvest()
		plant(Entities.Sunflower)
		measureRecord()
		createPath()
		harvestAll()
		resetPositionPetals()

if __name__ == "__main__":
	clear()
	def job():
		doSunflowers((0, 0), (3, 3))
	#job()
	spawn_drone(job)
	utils.goto(10, 10)
	while True:
		do_a_flip()
