a = [[0.01, 0.01, 0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.31, 0.01, 0.01, 0.01, 0.31, 0.31, 0.01, 0.01], [0.1225, 0.1225, 0.01, 0.1225, 0.1225, 0.1225, 0.1225, 0.1225, 0.01, 0.1225], [0.01, 0.01, 0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.46, 0.01, 0.01, 0.01, 0.46, 0.01, 0.01, 0.01], [0.01, 0.31, 0.31, 0.01, 0.01, 0.31, 0.01, 0.01, 0.01, 0.01], [0.01, 0.31, 0.31, 0.01, 0.01, 0.01, 0.01, 0.01, 0.31, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.91, 0.01, 0.01], [0.01, 0.01, 0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]]

b = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def mult_matrix(a, b):
	new_matrix = []
	sum = 0


	if len(a) == 0 or len(b) == 0:
		return None

	# create a now matrix that has the number of rows of a and number of cols of b, fill all element as 0
	for row_a in range(len(a)):
		new_matrix.append([])
	for col_b in range(len(b[0])):
		for row_a in range(len(a)):
			new_matrix[row_a].append(0)

	for row_a in range(len(a)):
		for col_b in range(len(b[0])):
			for row_b in range(len(b)):
				new_matrix[row_a][col_b] += a[row_a][row_b] * b[row_b][col_b]

	return new_matrix

print(mult_matrix(a, b))
