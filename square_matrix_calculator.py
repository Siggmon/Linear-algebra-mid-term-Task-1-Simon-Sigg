def get_sub_matrix(matrix, row): #returns the matrix, without the first column and without the row, given when called
    sub = []
    for i in range(len(matrix)):
        if i != row: #adds the rows to the submatrix, that are not the one, given when called
            sub.append(matrix[i][:])
    for i in range(len(sub)):
        del(sub[i][0]) #deletes the first column of the sub matrix
    return sub

#def get_determinant(matrix): Initial idea inspired by: "https://stackoverflow.com/questions/63660579/getting-n-x-n-matrix-determinant-in-c"
def get_determinant(matrix):
    if len(matrix) == 1: #the given matrix has only one entry(one row -> one entry, because it is a square matrix, got checked when user gave matrix): return entry
        det = matrix[0][0]
        return det
    elif len(matrix) == 2: #given matrix has 2 rows: calculate determinant with formula for 2x2 matrices (a*d - c*b)
        det = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return det
    elif len(matrix) == 3: #given matrice has 3 rows: calculate determinant with formula for 3x3 matrices (a*e*i + b*f*g + c*d*h - g*e*c - h*f*a - i*d*b
        det = matrix[0][0]*matrix[1][1]*matrix[2][2] + matrix[0][1]*matrix[1][2]*matrix[2][0] + matrix[0][2]*matrix[1][0]*matrix[2][1] - matrix[2][0]*matrix[1][1]*matrix[0][2] - matrix[2][1]*matrix[1][2]*matrix[0][0] - matrix[2][2]*matrix[1][0]*matrix[0][1]
        return det
    else: #given matrix has more then 3 lines: adds the determinants of the submatrices together(submatrix: matrix, without one line and without the first column, this is done for every line once)
        det = 0
        for row in range(len(matrix)):
            det = det + ((-1) ** row) * matrix[row][0] * get_determinant(get_sub_matrix(matrix, row)) #z.B 5x5 matrix: ads determinants of the five submatrices(4x4), which gets calculated by adding the determinants of the 20 submatrices(3x3) from the 5 submatrices(4x4) 
        return det

solve = input("Do you want to solve an equation system? (y/n): ")
while solve not in ("y", "n"):
    solve = input(f"{solve} is not a valid answer. Only y or n are valid answers(y=yes, n=no)\nTry again: ")
    
matrix = [] #[row, column]
matrix.append((input(f"1. Row(entrys sepperated by \",\"): ")).split(",")) #gets the first row of the matrix
for j in range(len(matrix[0])):
        matrix[0][j] = float(matrix[0][j]) #in first row are only floats
for i in range(len(matrix[0])-1):   #gets as many more rows as entrys in the first row(-> square matrix)
    matrix.append((input(f"{i+2}. Row(entrys sepperated by \",\"): ")).split(","))
    for j in range(len(matrix[i])):
        matrix[i+1][j] = float(matrix[i+1][j])  #every entry is a float
    if(len(matrix[i+1])) != len(matrix[0]): #one row is not the same row as the first row -> not square matrix -> error
        print("Matrix isn't invertible!")
        quit()

#gets right hand side vector b
if solve == "y":
    vec_b = input(f"Vector b(entrys sepperated by \",\" and has excactly {len(matrix)} entries): ").split(",")
    for i in range(len(vec_b)):
        vec_b[i] = float(vec_b[i])
    if len(vec_b) != len(matrix): #vector has not as many entries as the matrix has rows -> cant solve the system with it
        print("The vector has not the right ammount of entries!")
        quit()

#Check if the matrix is reversible
determinant = get_determinant(matrix)
if determinant == 0: #determinant is 0 -> singular, not invertible -> Report and quit
    print("This matrix is singular. It is not invertible!")
    quit()

#Produce an identity matrix with the same size as the input matrix
i_matrix = []
for i in range(len(matrix)):
    i_matrix.append([])
    for j in range(len(matrix)):
        i_matrix[i].append(0)
    i_matrix[i][i] = 1

#Step 5 of Gauss Algorithm
for pivot in range(len(matrix)): #I add pivot to the "coordinats" that use items from matrix, to move the pivot diagonally down to the right, until it is in the corner.  
    
    #Step 1 of Gauss Algorithm
    move_pivot = True
    for j in range(len(matrix)-pivot):
        for i in range(len(matrix)-pivot):
            if matrix[i+pivot][j+pivot] != 0.0 and move_pivot == True: #"Coordinats" of first element that is not == 0 gets saved, checks column after column
                move_pivot = False
                pivot_not_zero = [i+pivot,j+pivot] #[row, column]
    
    #Step 2 of Gauss Algorithm
    if pivot_not_zero[0] != 0 + pivot: #row with the first non 0 element is not the row where the pivot position is -> interchange row with row where the pivot element is (same operation with i_matrix)
        row = matrix[0+pivot]
        matrix[0+pivot] = matrix[pivot_not_zero[0]]
        matrix[pivot_not_zero[0]] = row

        row = i_matrix[0+pivot] #excactly the same row operation as above, but with the identity matrix
        i_matrix[0+pivot] = i_matrix[pivot_not_zero[0]]
        i_matrix[pivot_not_zero[0]] = row
    
    #Step 3 of Gauss Algorithm
    if matrix[0+pivot][pivot_not_zero[1]] != 1.0: #element with pivot position is not 1 -> row with pivot position * 1/element with pivot position
        factor = 1/matrix[0+pivot][pivot_not_zero[1]]
        for i in range(len(matrix[0])):
            matrix[0+pivot][i] = matrix[0+pivot][i] * factor #row with pivot position * 1/element with pivot position
            i_matrix[0+pivot][i] = i_matrix[0+pivot][i] * factor #same row with same factor, but with i_matrix

    #Step 4 of Gauss Algorithm
    for i in range(len(matrix)):
        if matrix[i][pivot_not_zero[1]] != 0.0 and i != pivot: #If any element in the column with the pivot position(except the one with the pivot position) isn't == 0: 
            factor = matrix[i][pivot_not_zero[1]]               
            for j in range(len(matrix[i])):        #row with element that isnt 0 - (element*pivot row)
                matrix[i][j] = matrix[i][j] - (factor * matrix[0+pivot][j]) 
                i_matrix[i][j] = i_matrix[i][j] - (factor * i_matrix[0+pivot][j]) #same row with same factor, but with i_matrix
    
print(f"Inverse: {i_matrix}")

if solve == "y":
    solution = []
    for i in range(len(matrix)): #Matrix with 4 rows -> solution has 4 rows
        entry = 0
        for j in range(len(vec_b)):
            entry = entry + i_matrix[i][j]*vec_b[j] #i. row gets calculated(vector[0]*matrix[i][0] + vector[1]*matrix[i][1] ... + vector[j]*matrix[i][j])
        solution.append(entry) #add to solution, 1. row is x, 2. is y, ...
    print(f"The solution(s) are: ")
    for i in range(len(solution)):
        print(f"X{i+1} = {solution[i]}") #prints the solutions, x1, x2, x3 are not possible values for x, they are seperate variables, like x, y, z, ...