import sunflowers
import serpentine
import f2
import lists
import utils
import positions

history = [(0,0), (0,0), (0,0), (0,0)]
if __name__ == "__main__":

	def followBot():
		quick_print("bot going to ", history)

	while(True):
		while(get_pos_x() != 11):
			quick_print(history)
			move(East)
			history.remove(history[0])
			history.append(positions.getPos())
			spawn_drone(followBot)
		while(get_pos_x() != 0):
			move(West)
			history.remove(history[0])
			history.append(positions.getPos())
	