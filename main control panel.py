import sunflowers
import serpentine
import f2

if __name__ == "__main__":
	clear()
	def job():
		sunflowers.doSunflowers((0, 0), (3, 3))
	spawn_drone(job)
	def job2():
		serpentine.serpentine(f2.makeHarvestFunction(Entities.Grass), (4, 0), (11, 4))
	spawn_drone(job2)
	def job3():
		do_a_flip()
		do_a_flip()
		serpentine.serpentine(f2.makeHarvestFunction(Entities.Grass), (0, 4), (11, 11))
	spawn_drone(job3)
		
	#serpentine.serpentine(f2.makeHarvestFunctionWithDecider(f2.plantAllWood), (0, 4), (11, 11))
	serpentine.serpentine(f2.makeHarvestFunction(Entities.Grass), (0, 4), (11, 11))