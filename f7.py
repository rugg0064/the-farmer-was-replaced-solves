import sunflowers
import serpentine
import f2

if __name__ == "__main__":
	clear()
	
	def genJob(boundsMin, boundsMax):
		def f():
			sunflowers.doSunflowers(boundsMin, boundsMax)
		return f
	spawn_drone(genJob((0, 0), (5, 5)))
	spawn_drone(genJob((5, 5), (11, 11)))
	spawn_drone(genJob((0, 5), (5, 11)))
	genJob((5, 0), (11, 5))()
