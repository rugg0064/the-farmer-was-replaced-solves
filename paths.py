import positions

# Returns an array of directions
def pathToDirections(path, withFinal = False):
	dirs = []
	for i in range(len(path) - 1):
		dirs.append(positions.directionToPosition(path[i+1], path[i]))
	if withFinal:
		dirs.append(positions.directionToPosition(path[0], path[len(path)-1]))
	return dirs

# Returns a dict that maps each position to the next position
def pathToDict(path, withFinal = False):
	dirs = {}
	for i in range(len(path) - 1):
		dirs[path[i]] = path[i+1]
	if withFinal:
		dirs[len(path)-1] = path[0]
	return dirs

# Returns a dict that maps each position inside the path to the direction to get to the next position
def pathToDirDict(path, withFinal):
	dirs = {}
	for i in range(len(path) - 1):
		dirs[path[i]] = positions.directionToPosition(path[i+1], path[i])
	if withFinal:
		dirs[path[len(path)-1]] = positions.directionToPosition(path[0], path[len(path)-1])
	return dirs

# Returns an array of points based on a path but shifts the start to pos
# Path will return from the first entry of that position in the array if it occurs twice
def pathStartAt(path, pos):
	newPath = []
	start = 0
	for i in range(len(path)):
		if path[i] == pos:
			start = i
	for i in range(start, len(path)):
		newPath.append(path[i])
	for i in range(0, start):
		newPath.append(path[i])
