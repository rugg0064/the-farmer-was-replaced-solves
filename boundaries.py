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
def getSize(bounds):
	d = positions.aToB(getMin(bounds), positions.add(getMax(bounds), (1, 1)))
	return positions.getX(d) * positions.getY(d)

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
