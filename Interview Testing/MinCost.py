'''
Code to take in an array as a string, convert it to a weighted matrix and then
find the minimum cost to travel from point (0,0) to point (m,n).

The basic idea here is to gradually fill out the array of lowest possible costs,
then grab the value at the point (m,n). We fill out the first row and column and
then build the rest of the matrix from there.

Algorithm ideas taken from geeksforgeeks for studying help. Done purely as practice
for interviews, not for class.
'''

#String parser array my own addition and not from geeksforgeeks. Takes in a string
#and creates a matrix of integers to use with the minimum_cost function
def create_array(matrix_string):
    list_of_rows = matrix_string.split(";")
    matrix_array = []
    for col in list_of_rows:
        new_item = col.split(',')
        new_item = [int(item) for item in new_item] #Should cast list of strings into a list of ints
        matrix_array.append(new_item)
    return matrix_array

def minimum_cost(matrix_array, m, n):
    total_cost = [[0 for x in range(m)] for x in range(n)] #creates all 0's total cost array same size as the matrix_array
    total_cost[0][0] = matrix_array[0][0] #initialize the value of the top left corner

    for i in range(1, m): #Initalize the value of the first column by adding up the values as you go down
        print(i)
        total_cost[i][0] = total_cost[i-1][0] + matrix_array[i][0]

    for j in range(1, n): #Repeat the prior step with the first row
        total_cost[0][j] = total_cost[0][j-1] + matrix_array[0][j]

    for i in range(1, m):
        for j in range(1, n):
            #need to find min value of the cells immediately above or to the left, along with diagonal cell
            total_cost[i][j] = min(total_cost[i-1][j-1], total_cost[i][j-1], total_cost[i-1][j]) + matrix_array[i][j]

    return total_cost[m-1][n-1]

if __name__ == "__main__":
    matrix_string = "1,2,3;4,5,6;7,8,9"  #corresponds to matrix where top row has weights (1,2) and bottom row is (3,4)
    matrix_array = create_array(matrix_string)
    for row in matrix_array:
        print(row)
    m = 3 #I manually define here which point I want to find the min cost to, m = column
    n = 3 # n = row
    print(minimum_cost(matrix_array, m, n))
