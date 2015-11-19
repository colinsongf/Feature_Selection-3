from pprint import pprint
import random

# constants for easy testing
# instances[i][0] is class name

def LoadData(file_name, num_instances):
    try:
        f = open(file_name, 'r')
    except:
        raise FileNotFoundError(file_name)
    instances = [[] for i in range(num_instances)]
    for i in range(num_instances):
        instances[i] = [float(j) for j in f.readline().split()]
    return instances

def OneOutCrossValidation(data, current_set, feature_to_add):
    """
    Subject to change:
    data is n-1 instances set with m features
    current_set is the instance that is out for testing
    feature_to_add is the feature to be tested
    """
    accuracy = random.randint(0, 100)
    return accuracy

def ForwardSelection(data, num_instances):
    pass

def BackwardElimination(data, num_instances):
    pass

def CustomSearch(data, num_instances):
    """
    Plan to use simulated annealing:
    It can give better results, but might be slower
    How to make it quicker?
    Use heuristic that favors the second best feature of
    the previous search when searching current features
    Might be quicker, but is it admissible? NO CLUE
    But since we're favoring the second best feature -- probably
    """
    pass

def NearestNeighbor(data, current_set):
    pass

def main():
    file_name = input("Enter the name of the file to test: ")
    num_instances = int(input("Enter the number of instances to read: "))
    instances = LoadData(file_name, num_instances)

    alg = ""
    while (alg != "FS" and alg != "BE" and alg != "CS"):
        alg = input("""Type in the algorithm you want to run:
                       FS - Forward Selection
                       BE - Backward Elimination
                       CS - Custom Search
                    \r""")
    print("There are %d features with %d instances." % (len(instances[0]) - 1, num_instances))
    pprint(instances)

if __name__ == '__main__':
    main()
