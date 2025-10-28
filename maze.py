import utils
import lists
import positions
# Returns (solved, newly checked positions)
# backtrackDirection is the move necessary to get to the parent state, None is allowed
def solveMazeHelper(
	traversedPositions,
	backtrackDirection,
	depth,
	endPosition,
):
	# quick_print("at depth " + str(depth))
	# quick_print(traversedPositions)
	# quick_print("Adding " + str(positions.getPos()))
	traversedPositions.add(positions.getPos())
	if positions.areEqual(positions.getPos(), endPosition):
	#if get_entity_type() == Entities.Treasure:
		harvest()
		return (True, traversedPositions)
	# Data type (direction, distance)
	choices = []
	for dir in utils.allDirections:
		# quick_print("Checking " + str(dir))
		if not can_move(dir):
			# quick_print("Can't move, skipping")
			continue
		# Position we want to explore
		goalPos = utils.tupleAdd(positions.getPos(), utils.directionToTuple[dir])
		# Don't explore entries we've already checked
		if goalPos in traversedPositions:
			#quick_print("Already traversed that position")
			continue
		distance = positions.manhattanDistance(goalPos, endPosition)
		choices.append((dir, distance))
	# Sort choices so min distance is first
	def choiceComparator(a, b):
		return lists.numAscend(a[1], b[1])
	choices = lists.mergeSort(choices, choiceComparator)
	#quick_print("Sorted choices", choices)
	# Move according to the sorted order
	for choice in choices:
		dir = choice[0]
		move(dir)
		# quick_print("recursing " + str(dir))
		solved, traversedPositions = solveMazeHelper(traversedPositions, utils.oppositeDirection[dir], depth + 1, endPosition)
		# If solved bubble up answer
		if solved:
			return solved, traversedPositions
	utils.moveNone(backtrackDirection)
	# quick_print("Failed to solve, reverting, " + str(traversedPositions))
	return False, traversedPositions

def solveMaze():
	# We ignore this direction provided
	endPosition = measure()
	solveMazeHelper(set(), None, 0, endPosition)
	
# Uses maze solving algorithm to path find to a location
def gotoPathfind(endPosition):
	solveMazeHelper(set(), None, 0, endPosition)


def doMazing(home):
	while True:
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, maze_price(6))	
		solveMaze()
		utils.goto(home[0], home[1])

def makeDoMazing(home):
	def f():
		doMazing(home)
	return f

def maze_price(size):
	return size * 2**(num_unlocked(Unlocks.Mazes) - 1)

def main():
	clear()
	plant(Entities.Grass)
	spawn_drone(makeDoMazing([11,11]))
	spawn_drone(makeDoMazing([0,11]))
	spawn_drone(makeDoMazing([11,0]))
	doMazing([0, 0])
# main()
if __name__ == "__main__":
	main()