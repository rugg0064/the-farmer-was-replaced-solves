clear()
till()
plant(Entities.Pumpkin)
while True:
	do_a_flip()
	quick_print(can_harvest())
	quick_print(measure())
	if can_harvest():
		harvest()
		plant(Entities.Pumpkin)