
def solveMaze():
	# (x,y) tuple
	goal = measure()
	moveStack = []
	# TODO: Try changing to a set
	exploredPositions = {getPos()}
	backtrack = []
	

	

	
	def addOptions():
		global moveStack
		global exploredPositions
		for dir in [North, East, South, West]:
			dirPos = tupleAdd(getPos(), directionToTuple[dir])
			if dirPos not in exploredPositions:
				if can_move(dir):
					move
		