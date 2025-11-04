# Bounds is generally a tuple ( (x1, y1), (x2, y2) ) and represents an inclusive bounding box

import positions
import directions
import utils 

def getWorldBounds():
	return ((0, 0), (get_world_size() - 1, get_world_size() - 1))

# Returns true if 
# pos is a Positions
# direction is a Direction
def isAtEdge(bounds, direction, pos = positions.getPos()):
	if directions.isHorizontal(direction):
		x = get_pos_x()
		if direction == West:
			return x == bounds[0][0]
		else:
			return x == bounds[1][0]
	else:
		y = get_pos_y()
		if direction == South:
			return y == bounds[0][1]
		else:
			return y == bounds[1][1]

def isInBounds(bounds, pos = positions.getPos()):
	return positions.getX(pos) >= positions.getX(getMin(bounds)) and positions.getX(pos) <= positions.getX(getMax(bounds)) and positions.getY(pos) >= positions.getY(getMin(bounds)) and positions.getY(pos) <= positions.getY(getMax(bounds))

def getMin(bounds):
	return bounds[0]
def getMax(bounds):
	return bounds[1]
def getBottomLeft(bounds):
	return bounds[0]
def getBottomRight(bounds):
	return (bounds[1][0], bounds[0][1])
def getTopLeft(bounds):
	return (bounds[0][1], bounds[1][0])
def getTopRight(bounds):
	return bounds[1]
# Returns the size in number of squares as (x,y)
def getSize(bounds):
	return positions.aToB(getMin(bounds), positions.add(getMax(bounds), (1, 1)))
def getArea(bounds):
	d = getSize(bounds)
	return positions.getX(d) * positions.getY(d)
def getWidth(bounds):
	return positions.aToB(getBottomLeft(bounds), getTopRight(bounds))[0]+1
def getHeight(bounds):
	return positions.aToB(getBottomLeft(bounds), getTopRight(bounds))[1]+1


# bottomLeft is the starting point (x,y)
# size is the size(x,y)
def fromBottomLeft(bottomLeft, size):
	return ((bottomLeft), (positions.add(bottomLeft, positions.subtract(size, (1, 1)))))

def getDirectionToBounds(bounds, pos = positions.getPos()):
	if isInBounds(bounds, pos):
		return None
	# Argmin stack to find closest position, return direction towards that

	closestDist = positions.manhattanDistance(getBottomLeft(bounds), pos)
	closestPos = getBottomLeft(bounds)

	closestDist, closestPos = utils.argmin(
		closestDist,
		closestPos,
		positions.manhattanDistance(getBottomRight(bounds), pos), 
		getBottomRight(bounds)
	)

	closestDist, closestPos = utils.argmin(
		closestDist,
		closestPos,
		positions.manhattanDistance(getTopLeft(bounds), pos), 
		getTopLeft(bounds),
	)

	closestDist, closestPos = utils.argmin(
		closestDist,
		closestPos,
		positions.manhattanDistance(getTopRight(bounds), pos), 
		getTopRight(bounds),
	)

	quick_print("cps", closestPos)
	return positions.directionToPosition(closestPos)

# Returns a set of all positions
def getAllPositions(bounds):
	ret = set()
	for x in range(positions.getX(getMin(bounds)), positions.getX(getMax(bounds)) + 1):
		for y in range(positions.getY(getMin(bounds)), positions.getY(getMax(bounds)) + 1):
			ret.add((x,y))
	return ret

# Returns a copy of a boundary with the opposite edge pulled <direction> by <amount>. IE a 2x2 shrunk East will because a 1x2 with bottom-left moved East
# Does not error check
def shrink(bounds, direction, amount):
	if direction in {East, North}: # Shrink the min
		return ((positions.add(getBottomLeft(bounds), positions.mul(directions.directionToVector[direction], amount) )), (getTopRight(bounds)))
	else: # Shrink the max
		return (getBottomLeft(bounds), (positions.add(getTopRight(bounds), positions.mul(directions.directionToVector[direction], amount) )))

