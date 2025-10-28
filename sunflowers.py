import utils
import serpentine
import lists
import positions
import boundaries
import f2
import newSerpentine

SUNFLOWER_MAX_TIME = 8.4 

def positionPetalsComparator(a, b):
	return lists.numAscend(a[0], b[0])

def makeSunflowersJob(bounds):
	def f():
		doSunflowers(bounds)
	return f

def doSunflowers(bounds):
	positions.gotoPos(boundaries.getMin(bounds))
	# (pedals, position)
	positionPetals = []
	# First plant everything and get data in good state
	def plantJob():
		plant(Entities.Sunflower)
		lists.sortedInsert(positionPetals, (measure(), positions.getPos()), positionPetalsComparator)
		#quick_print(positionPetals, len(positionPetals))
		#quick_print(positionPetals)
	# Plants on bounds
	serpentine.doForAll(newSerpentine.makeSerpentinePlan(bounds, newSerpentine.SERPENTINE_MODE_VERTICAL),
					 f2.combineActions(utils.ensureTilled, plantJob), bounds)
	do_a_flip()
	# Harvesting loop
		
	def gotoWaitHarvest(pos):
		positions.gotoPos(best[1])
		while not can_harvest():
			do_a_flip()
		harvest()
	
	while True:
		replant = []
		while len(positionPetals) >= 10:
			# Go to best
			best = positionPetals.pop()
			gotoWaitHarvest(best[1])
			replant.append(best[1])
		# serpentine.doForAll(newSerpentine.makeSerpentinePlan(bounds, newSerpentine.SERPENTINE_MODE_VERTICAL),
		# 			 f2.combineActions(utils.ensureTilled, plantJob), bounds)
		for pos in replant:
			positions.gotoPos(pos)
			plantJob()

if __name__ == "__main__":
	clear()
	def job():
		doSunflowers((0, 0), (3, 3))
	#job()
	spawn_drone(job)
	utils.goto(10, 10)
	while True:
		do_a_flip()