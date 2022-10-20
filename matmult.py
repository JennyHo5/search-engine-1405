
# return a new 2D list containing the result when the given matrix is multiplied by the given scalar (i.e., a given integer/float value). The original matrix passed as an argument to the function must not be modified.
def mult_scalar(matrix, scale):
	new_matrix = []
	for i in range(len(matrix)):
		new_matrix.append([])
		for j in range(len(matrix[i])):
			new_index = matrix[i][j] * scale
			new_matrix[i].append(new_index)
	return new_matrix

# return a new matrix that is the result of multiplying the matrix a by the matrix b. The original matrix passed as an argument to the function must not be modified.
# rank = number of col in a = number of row in b
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

# This function accepts two single-row matrices (i.e., vectors) using the list representation for matrices used so far in this problem (e.g., a = [ [9, 3, 1] ]). Your function must calculate the Euclidean distance between these two vectors.
def euclidean_dist(a,b):
	if len(a[0]) == len(b[0]) and len(a[0]) != 0:
		sum = 0
		for i in range(len(a[0])):
			sum += (a[0][i] - b[0][i]) ** 2
		return sum ** (1/2)
	else:
		return None
