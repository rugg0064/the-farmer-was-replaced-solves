import mazes




def main():
	# Create the maze
	mazes.createMaze(6)
	# Build the maze graph
	graph = mazes.createInitialGraph()

if __name__ == '__main__':
	main()