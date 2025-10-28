

# Plan is a function that handles movement, each call should make one motion
# Action must be aware of whether or not it is in the zone that things should be run
def moveWithPlan(plan, action):
	while True:
		plan()
		action()
