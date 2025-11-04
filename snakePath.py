import boundaries
import directions
import positions
import lists

# Returns a path List<Pos> 
# The size of the bounds in startDirection must be even
# startDirection = Primary axis
def makeSnakePath(bounds, startPos, primaryDirection):
	secondaryDirection = None
	if directions.isHorizontal(primaryDirection):
		if boundaries.isInBounds(bounds, positions.add(startPos, directions.directionToVector[South])):
			# If south is in bounds use that
			secondaryDirection = South
		else:
			# It is in bounds, therefore North
			secondaryDirection = North
	else:
		quick_print("Vertical")
		if boundaries.isInBounds(bounds, positions.add(startPos, directions.directionToVector[East])):
			secondaryDirection = East
		else:
			secondaryDirection = West
	quick_print("sd", secondaryDirection)
	path = [startPos]
	curDir = primaryDirection
	curPos = positions.add(startPos, directions.directionToVector[curDir])
	snakeBounds = boundaries.shrink(bounds, primaryDirection, 1)
	next = None
	while next == None or not positions.areEqual(next, startPos):
		quick_print(path)
		# Go on primary axis until on last
		next = positions.add(curPos, directions.directionToVector[curDir])
		while boundaries.isInBounds(snakeBounds, next):
			path.append(curPos)
			curPos = next
			next = positions.add(curPos, directions.directionToVector[curDir])
		# Check if you can move along the secondary axis
		next = positions.add(curPos, directions.directionToVector[secondaryDirection])
		quick_print(snakeBounds, curPos, next, boundaries.isInBounds(snakeBounds, next))
		if boundaries.isInBounds(snakeBounds, next):
			# Yes can move to the side, do that and reverse main dir
			path.append(curPos)
			curPos = next
			curDir = directions.oppositeDirection[curDir]
		else:
			# Else we are at the end. So we progress one further into return lane and go home
			quick_print("Starting walk home", curPos, path, curDir)
			path.append(curPos)
			curPos = positions.add(curPos, directions.directionToVector[curDir])
			next = positions.add(curPos, directions.directionToVector[directions.oppositeDirection[secondaryDirection]])
			quick_print("Did step down", curPos, next)
			while not positions.areEqual(next, startPos):
				path.append(curPos)
				curPos = next
				next = positions.add(curPos, directions.directionToVector[directions.oppositeDirection[secondaryDirection]])
			path.append(curPos)
	return path



