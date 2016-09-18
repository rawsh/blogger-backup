l = []

for k in range(1,19):
	x = (k**9)%19
	if x in l:
		pass
	else:
		l.append(x)
print(sorted(l))
