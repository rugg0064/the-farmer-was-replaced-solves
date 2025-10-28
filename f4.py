import serpentine
import f2
import positions
import lists
import utils
# Optimized flowers

# Position, amount
check = []
def getIndex(pos):
	i = 0
	for entry in check:
		if positions.areEqual(entry[0], pos):
			return i
		i += 1
def checkAndAdd():
	global check
	check.append((positions.getPos(), measure()))
	#quick_print(check)
def sortPositions():
	def comparator(a, b):
		return lists.invert(lists.numAscend(a, b))
	global check
	check = lists.mergeSort(check, comparator)

# serpentine.doForAll(f2.makeHarvestFunction(Entities.Sunflower), boundsMin, boundsMax)

clear()
boundsMin = (1, 1)
boundsMax = (2, 2)
	
serpentine.doForAll(till, boundsMin, boundsMax)
def p():
	def f():
		plant(Entities.Sunflower)
	return f
serpentine.doForAll(p, boundsMin, boundsMax)

quick_print(checkAndAdd())
def f():
	checkAndAdd()
serpentine.doForAll(f, boundsMin, boundsMax)
#serpentine.serpentine(checkAndAdd, boundsMin, boundsMax)


