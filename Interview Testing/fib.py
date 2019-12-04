#recursive method to find the nth number of the Fibonacci sequence
#Potential interview question
def fibonacci(n):
    if n < 0:
        print("You have entered an invalid integer. Please choose a positive integer.")
        return -1
    if n <= 1:
        return n # NOTE: should only trigger for n=1 or n=0
    else:
        return fibonacci(n-1) + fibonacci(n-2)

#Method that builds off of fibonacci to find the first n numbers in the sequence
def fibonacci_list(n):
    first_n_nums = []
    for i in range(n):
        first_n_nums.append(fibonacci(i))
    return first_n_nums

#main function for testing
if __name__ == "__main__":
    n = int(input("Please choose a positive integer. "))
    print("The nth number is " + str(fibonacci(n)))
    print(fibonacci_list(n))
