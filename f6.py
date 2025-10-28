import sunflowers
import serpentine
import f2
import lists
import utils
import positions

def main():
	clear()

	def handler():
		goal = ()
		def randomize():
			global goal
			goal = (Entities.Grass, (random() * get_world_size() // 1, random() * get_world_size() // 1))
		randomize()
		unharvstableCount = 0
		while(True):
			quick_print("Handling companion", goal)
			while positions.isInBounds(goal[1], (0, 0), (21, 5)):
				quick_print("randominzing")
				randomize()
			positions.gotoPos(goal[1])
			if can_harvest():
				harvest()
			else:
				unharvstableCount += 1
			if unharvstableCount > 5:
				goal = (Entities.Grass, (random() * get_world_size() // 1, random() * get_world_size() // 1))
				quick_print("activating anti loop")
				unharvstableCount = 0
				continue
			if goal[0] == Entities.Carrot:
				utils.ensureGroundType(Grounds.Soil)
			plant(goal[0])
			goal = get_companion()
			if goal == None:
				randomize()
	for i in range(5):
		spawn_drone(handler)
	
	def makeSunflowerJob(bounds):
		def f():
			sunflowers.doSunflowers(bounds[0], bounds[1])
		return f

	spawn_drone(makeSunflowerJob(((0, 0), (10, 5))))
	spawn_drone(makeSunflowerJob(((11, 0), (21, 5))))

	# while True:
	# 	do_a_flip()
	#stack = []
	#plant(Entities.Grass)
	#stack.insert(0, Entities.Grass)
	
	

if __name__ == "__main__":
	main()	


