# Tools for sets

# Reports entries that are in s2 but not s1
def diff(s1, s2):
	ret = set()
	for entry in s2:
		if entry not in s1:
			ret.add(entry)
	return ret
