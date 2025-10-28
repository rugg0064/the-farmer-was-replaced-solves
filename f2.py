import serpentine
import utils


global vertical	
global lastDirection

def doOnSome(do, task):
	goHome()
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			if do():
				task()
			move(East)
		move(North)

def doOnAll(task):
	goHome()
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			task()
			move(East)
		move(North)
	
def plantAndHarvest(entity):
	# plant(entity)
	harvestIfPossible()
	plant(entity)

# Entity Decider is a function that takes no arguments and returns an Entity
# f() => Entity
#def plantAndHarvestWithDecider(entityDecider):
#	plantAndHarvest(

def makeHarvestFunction(entity):
	def f():
			plantAndHarvest(entity)
	return f
def harvestIfPossible():
	#if not can_harvest():
	#	if get_entity_type() == Entities.Tree:
	#		use_item(Items.Fertilizer)
	if can_harvest():
		harvest()
		
# Decider: f() => Entity
def makeHarvestFunctionWithDecider(decider):
	def f():
		plantAndHarvest(decider())
	return f
def withDecider(decisionFunc):
	return makeHarvestFunction(whatToPlant)

def whatToPlantAllWood():
	x = get_pos_x()
	y = get_pos_y()
	if x%2 == y%2:
		return Entities.Tree
	else:
		return Entities.Bush

def whatToPlant():
	x = get_pos_x()
	y = get_pos_y()
	if x >= 3 and y <= 2:
		return Entities.Pumpkin
	if x%2 == y%2:
		return Entities.Tree
	return Entities.Carrot

def plantAllWood():
	x = get_pos_x()
	y = get_pos_y()
	if x%2 == y%2:
		return Entities.Tree
	else:
		return Entities.Bush
	

def tillSome():
	def where():
		return get_pos_x() >= 2 and get_pos_y() <= 3
	doOnSome(where, till)

def combineActions(a, b):
	def f():
		a()
		b()
	return f

if __name__ == "__main__":
	clear()
	#doOnAll(till)
	#tillSome()
	utils.goHome()
	#serpentine(makeHarvestFunction(Entities.Grass))
	#serpentine(makeHarvestFunction(Entities.Carrot))
	serpentine.doForAll(till, (2,2), (4,4))
	def printCheck():
		quick_print(measure())
	serpentine.serpentine(combineActions(printCheck, makeHarvestFunction(Entities.Sunflower)), (2, 2), (4, 4))
	#serpentine.serpentine(makeHarvestFunctionWithDecider(whatToPlant), (2, 2), (4, 4))