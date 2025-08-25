def func (x, y):
	if (x == 10):
		print('Variable x is 10.')
	else:
		if (y == 3):
			print('Variable x is not 10 but variable y is 3.')
		else:
			print('Variable x is not 10 and variable y is not 3.')
			return 1
x = 10
y = 2
print(func(x, y))
