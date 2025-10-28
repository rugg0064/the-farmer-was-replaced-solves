import boundaries
import directions 

SERPENTINE_MODE_VERTICAL = 1
SERPENTINE_MODE_HORIZONTAL = 2

# bounds is ( (x1, y1), (x2, y2) ) inclusive
# mode is SERPENTINE_MODE. 
# It means the priority of movement. 
# Horizontal means it will go horizontal, and then jump to the next row.
# Vertical means it will go up and down, and shift columns

# Returns a movement plan, returns func() None
# Each call will advance the drone by 0 or 1 steps.
def makeSerpentinePlan(bounds, mode):
	# Metadirection is the direction we go whenever we hit an edge to start the next run
	metaDirection = North
	lastDirection = East
	if mode == SERPENTINE_MODE_VERTICAL:
		metaDirection = East
		lastDirection = North
	# Move the drone and record last direction
	def moveAndSet(direction):
		global lastDirection
		move(direction)
		lastDirection = direction
	# Useful for when we just moved to a new row
	def moveNewRow():
		if mode == SERPENTINE_MODE_VERTICAL:
			if boundaries.isAtEdge(bounds, North):
				moveAndSet(South)
			else:
				moveAndSet(North)
		else:
			if boundaries.isAtEdge(bounds, East):
				moveAndSet(West)
			else:
				moveAndSet(East)
	def isModeDirection(direction):
		if mode == SERPENTINE_MODE_HORIZONTAL:
			return direction == West or direction == East
		else:
			return direction == North or direction == South
	def serpentineStep():
		global metaDirection
		if not boundaries.isInBounds(bounds):
			move(boundaries.getDirectionToBounds(bounds))
			return
		if boundaries.isAtEdge(bounds, lastDirection):
			if isModeDirection(lastDirection):
				if boundaries.isAtEdge(bounds, metaDirection):
					metaDirection = directions.getOpposite(metaDirection)
				moveAndSet(metaDirection)
			else:
				moveNewRow()
			return
		if not isModeDirection(lastDirection):
			moveNewRow()
			return
		# If we just moved to the next row/col
		if lastDirection == metaDirection:
			moveNewRow()
			return
		move(lastDirection)
	return serpentineStep
