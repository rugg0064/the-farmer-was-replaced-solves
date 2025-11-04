import sunflowers
import serpentine
import f2
import utils
import positions
import boundaries

# Creates function that can be run every tile for pumpkin
def getPumpkinAction(bounds):
	pumpkinSet = set()
	def f():
		global pumpkinSet
		if not boundaries.isInBounds(bounds):
			return pumpkinSet
		utils.ensureTilled()
		if get_entity_type() == Entities.Dead_Pumpkin:
			harvest()
			plant(Entities.Pumpkin)
			return pumpkinSet
		if get_entity_type() == None:
			plant(Entities.Pumpkin)
		if can_harvest():
			pumpkinSet.add(positions.getPos())
		if len(pumpkinSet) == boundaries.getArea(bounds):
			use_item(Items.Fertilizer)
			harvest()
			pumpkinSet = set()
		return pumpkinSet
	return f

def doBigPumpkin(bounds):
	serpentine.doForAll(utils.ensureTilled, boundaries.getMin(bounds), boundaries.getMax(bounds))
	# Contains positions
	pumpkinSet = set()
	def f():
		# quick_print(pumpkinSet)
		global pumpkinSet
		if get_entity_type() == Entities.Dead_Pumpkin:
			harvest()
			plant(Entities.Pumpkin)
			return
		if get_entity_type() == None:
			plant(Entities.Pumpkin)
		if can_harvest():
			pumpkinSet.add(positions.getPos())
		if len(pumpkinSet) == boundaries.getArea(bounds):
			harvest()
			pumpkinSet = set()
	serpentine.serpentine(f, boundsMin, boundsMax)
	
def makeDoBigPumpkinJob(bounds):
	def f():
		doBigPumpkin(bounds)
	return f

if __name__ == "__main__":
	clear()

	makeDoBigPumpkinJob(boundaries.getWorldBounds())()

	#spawn_drone(makeDoBigPumpkinJob((0, 7), (4, 11)))
	#spawn_drone(makeDoBigPumpkinJob((7, 0), (11, 4)))
	#spawn_drone(makeDoBigPumpkinJob((6, 6), (11, 11)))
	#doBigPumpkin(boundsMin, boundsMax)
		