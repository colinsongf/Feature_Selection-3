from pprint import pprint
from sklearn import

# constants for easy testing
# instances[i][0] is class name
my_file_name = "cs_170_small1.txt"
my_num_instances = 100

# arbitrary functions
def LoadData(file_name, num_instances):
    f = open(file_name, 'r')
    instances = [[] for i in range(num_instances)]
    for i in range(num_instances):
        instances[i] = [float(j) for j in f.readline().split()]

    return instances

# start here
file_name = input("Enter the name of the file to test: ")
num_instances = int(input("Enter the number of instances to read: "))
instances = LoadData(my_file_name, my_num_instances)
alg = input("""Type in the algorithm you want to run:
               FS - Forward Selection
               BE - Backward Elimination
               CS - Custom Search
            \r""")
print("There are %d features with %d instances." % (len(instances[0]) - 1, num))
