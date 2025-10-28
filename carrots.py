import sunflowers
import serpentine
import f2
import utils
import positions


def doCarrots(boundsMin, boundsMax):
	serpentine.doForAll(utils.ensureTilled, boundsMin, boundsMax)
	serpentine.serpentine(f2.makeHarvestFunction(Entities.Carrot), boundsMin, boundsMax)

def makeDoBigPumpkinJob(boundsMin, boundsMax):
	def f():
		for _ in range(random() * 20 // 1):
			do_a_flip()
		doCarrots(boundsMin, boundsMax)
	return f

if __name__ == "__main__":
	clear()
	for i in range(3):
		spawn_drone(makeDoBigPumpkinJob((0, 0), (11, 11)))
		
	doCarrots((0, 0), (11, 3))