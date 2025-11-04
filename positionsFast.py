# Functions regarding positions
# Positions are tuples (x, y)
# Also doubles as a Vector

import utils

def manhattanDistance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Subtracts two positions a - b
def subtract(a, b):
	return (getX(a) - getX(b), getY(a) - getY(b))

def add(a, b):
	return (getX(a) + getX(b), getY(a) + getY(b))

# Returns (|a|, |b|)
def absPosition(a):
	return (abs(getX(a)), abs(getY(a)))

# Returns a Vector from a to b
def aToB(a, b):
	return subtract(b,a)

def mul(a, x):
	return (getX(a) * x, getY(a) * x)

def areEqual(p1, p2):
	return p1[0]==p2[0] and p1[1]==p2[1]
	
def gotoPos(p):
	utils.goto(p[0], p[1])

# Returns an (x,y) tuple of the current position	
def getPos():
	return (get_pos_x(), get_pos_y())

def getX(position):
	return position[0]

def getY(position):
	return position[1]

# Returns the Direction to get from fromPos to toPos
# Biases to whichever direction is further, and biases horizontal
def directionToPosition(toPos, fromPos = getPos()):
	if areEqual(fromPos, toPos):
		return None
	diff = aToB(fromPos, toPos)
	# True if horizontal is bigger
	if abs(getX(diff)) >= abs(getY(diff)):
		if getX(diff) >= 0:
			return East
		else:
			return West
	else:
		if getY(diff) >= 0:
			return North
		else:
			return South

