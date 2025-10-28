# Helper functions that involve the Directions class

def isVertical(direction):
	return direction == North or direction == South

def isHorizontal(direction):
	return direction == East or direction == West
def getOpposite(direction):
	if direction == East:
		return West
	if direction == West:
		return East
	if direction == North:
		return South
	if direction == South:
		return North
	
oppositeDirection = {
	North:South,
	East:West,
	South:North,
	West:East,
}

directionToVector = {
	North:(0,1),
	East:(1,0),
	South:(0,-1),
	West:(-1,0)		
}

allDirections = [North, East, South, West]