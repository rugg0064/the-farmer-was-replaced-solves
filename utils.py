

# Adds two (x, y) tuples
def tupleAdd(a, b):
		return (a[0] + b[0], a[1] + b[1])
		
# None-tolerant move command
def moveNone(dir):
	if dir != None:
		move(dir)

# Goes to position in a straight line
def goto(x, y):
	# quick_print(get_pos_x(), get_pos_y(), x, y)
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

# Goes to 0,0
def goHome():
	while get_pos_x() != 0:
		move(West)
	while get_pos_y() != 0:
		move(South)
	
def ensureGroundType(groundType):
	if get_ground_type() != groundType:
		till()
		
def ensureTilled():
	if get_ground_type() != Grounds.Soil:
		till()
	
def ceil(x):
	if x > x//1:
		return (x//1)+1	

# compares xValue (av, bv)
# choses xItem (ai, bi) with lower associated value and returns xv xi
def argmin(av, ai, bv, bi):
	if av < bv:
		return av, ai
	return bv, bi
	
def argmax(av, ai, bv, bi):
	if av > bv:
		return av, ai
	return bv, bi