import maze
import positions 
import utils
import positions
import boundaries
# Action runs on each tile
# boundsMin and boundsMax are bounding box tuples (x,y) both numbers are inclusive
def serpentine(action, boundsMin, boundsMax):
	vertical = North
	lastDirection = East
	def moveAndSet(direction):
		global lastDirection
		move(direction)
		lastDirection = direction
	def isVertical(direction):
		return direction == North or direction == South
	def isHorizontal(direction):
		return direction == East or direction == West
	# Considering the bounds
	def isAtEdge(direction):
		if isHorizontal(direction):
			x = get_pos_x()
			if direction == West:
				return x == boundsMin[0]
			else:
				return x == boundsMax[0]
		else:
			y = get_pos_y()
			if direction == South:
				return y == boundsMin[1]
			else:
				return y == boundsMax[1]
	def moveAwayHorizontal():
		if isAtEdge(East):
			moveAndSet(West)
			return
		else:
			moveAndSet(East)
			return
	def opposite(direction):
		if direction == East:
			return West
		if direction == West:
			return East
		if direction == North:
			return South
		if direction == South:
			return North
	def serpentineStep():
		if get_pos_x() < boundsMin[0]:
			move(East)
			return
		if get_pos_x() > boundsMax[0]:
			move(West)
			return
		if get_pos_y() < boundsMin[1]:
			move(North)
			return
		if get_pos_y() > boundsMax[1]:
			move(South)
			return
		global vertical
		if isAtEdge(lastDirection):
			if isHorizontal(lastDirection):
				if isAtEdge(vertical):
					vertical = opposite(vertical)
				moveAndSet(vertical)
				return
			else:
				moveAwayHorizontal()
				return
		if isVertical(lastDirection):
			moveAwayHorizontal()
			return
		move(lastDirection)
	while True:
		if positions.isInBounds(positions.getPos(), boundsMin, boundsMax):
			action()
		serpentineStep()

def doForAll(movementPlan, action, bounds):
	size = boundaries.getArea(bounds)
	positionsDone = set()
	while len(positionsDone) != size:
		action()
		positionsDone.add(positions.getPos())
		movementPlan()