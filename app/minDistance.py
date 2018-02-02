def dist(source, target):
	n = len(source)+1
	m = len(target)+1

	matrix = []
	for i in range(n):
		row = []
		for j in range(m):
			row.append(0)
		matrix.append(row)

	for i in range(m):
		matrix[0][i] = i

	for i in range(n):
		matrix[i][0] = i
	
	for i in range(1,n):
		for j in range(1,m):
			matrix[i][j] = min(matrix[i-1][j]+1, matrix[i][j-1]+1, matrix[i-1][j-1] + sub(source[i-1],target[j-1]))

	#printMatrix(matrix)
	return matrix[-1][-1]

def sub(a, b):
	if a == b:
		return 0
	else:
		return 2

'''def printMatrix(mat):
	for i in mat:
		print i
'''
def mindistance(keyword, dictionary):	
	#dictionary = ['math', 'mathematics', 'software' ,'graphics']
	#keyword = 'graph'
	least = 100 
	distance_arr = []
	for i in dictionary:
		distance_arr.append(dist(keyword, i))
		#print dist(keyword, i), i

	return dictionary[distance_arr.index(min(distance_arr))]