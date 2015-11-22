from pprint import pprint
import random
import math

# instances[i][0] is class name
# instances[i][1] for feature 1
# instances[i][2] for feature 2...etc

def LoadData(file_name, num_instances):
    try:
        f = open(file_name, 'r')
    except:
        raise FileNotFoundError(file_name)
    instances = [[] for i in range(num_instances)]
    for i in range(num_instances):
        instances[i] = [float(j) for j in f.readline().split()]
    return instances

def NearestNeighbor(instances, num_instances, one_out, features):
    """
    Want to use scikitlearn nearest neighbor for learning purposes -- if I have time/not lazy
    """
    nearest_neighbor = -1
    nearest_neighbor_distance = float('inf')
    num_features = len(features)
    for i in range(0, num_instances):
        if (i == one_out):
            pass
        else:
            sum = 0
            for j in range(0, num_features):
                sum = sum + pow((instances[i][features[j]] - instances[one_out][features[j]]), 2)
            distance = math.sqrt(sum)
            if distance < nearest_neighbor_distance:
                nearest_neighbor_distance = distance
                nearest_neighbor = i
    return nearest_neighbor

def CheckClassification(instances, nearest_neighbor, one_out):
    if (instances[nearest_neighbor][0] != instances[one_out][0]):
        return False
    return True

def OneOutCrossValidation(instances, num_instances, current_features, feature_to_add):
    """
    Also want to use scikitlearn for learning purposes -- if I have time/not lazy
    """
    list_features = list(current_features)
    list_features.append(feature_to_add)
    num_correct = 0
    for i in range(0, num_instances):
        one_out = i
        nearest_neighbor = NearestNeighbor(instances, num_instances, one_out, list_features)
        correct_classification = CheckClassification(instances, nearest_neighbor, one_out)
        if (correct_classification):
            num_correct += 1
    accuracy = num_correct / num_instances
    return accuracy

def CalcMean(instances, num_instances, num_features):
    mean = []
    for i in range(1, num_features + 1): # Add one to exclude the class data
        mean.append((sum(row[i] for row in instances)) / num_instances)
    return mean

def CalcStd(instances, num_instances, num_features, mean):
    std = []
    for i in range(1, num_features + 1):
        std.append(math.sqrt((sum(pow((row[i] - mean[i-1]), 2) for row in instances)) / num_instances))
    return std

def NormalizeData(instances, num_instances, num_features):
    """ Calculates normalized data """
    normalized_instances = instances
    mean = CalcMean(normalized_instances, num_instances, num_features)
    std = CalcStd(normalized_instances, num_instances, num_features, mean)
    for i in range(0, num_instances):
       for j in range(1, num_features + 1):
           normalized_instances[i][j] = ((instances[i][j] - mean[j-1]) / std[j-1])
    return normalized_instances

def ForwardSelection(data, num_instances, num_features):
    current_set_of_features = set()
    for i in range(num_features):
        print("On %d level of the search tree" % (i+ 1))
        feature_to_add = 0
        best_so_far_accuracy = 0

        for j in range(num_features):
            if ((j + 1) not in current_set_of_features):
                print("Consider adding feature %d to set" % (j + 1))
                accuracy = OneOutCrossValidation(data, num_instances, current_set_of_features, j + 1)
                print("Accuracy: ", accuracy)

                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_add = j + 1

        current_set_of_features.add(feature_to_add)
        print("On %d level of the search tree, add feature %d" % ((i+1), feature_to_add))

    print("Best set of features to use: ", current_set_of_features)


def BackwardElimination(data, num_instances, num_features):
    current_set_of_features = set(i+1 for i in range(0, num_features))
    for i in range(num_features):
        print("On %d level of the search tree" % (i+1))
        feature_to_remove = 0
        best_so_far_accuracy = 0

        for j in range(num_features):
            if ((j+1) in current_set_of_features):
                print("Consider removing feature %d from set" % (j+1))
                accuracy = OneOutCrossValidation(data, num_instances, current_set_of_features, j+1)

                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_remove = j + 1

        current_set_of_features.remove(feature_to_remove)
        print("On %d level of the search tree, remove feature %d" % ((i+1), feature_to_remove))

    print("Best set of features to use: ", current_set_of_features)

def CustomSearch(data, num_instances, num_features):
    """
    Brainstorming stuff

    Plan to use simulated annealing:
    It can give better results, but might be slower
    How to make it quicker?
    Use heuristic that favors the second best feature of
    the previous search when searching current features
    Might be quicker, but is it admissible? NO CLUE
    But since we're favoring the second best feature -- probably

    Using projectspot.com as reference:
    Make a random set of features to use

    We can add or remove features, but it will take longer -- high branching factor
    Also have to keep track of states -- so better to stick with one way since
    we still can explore the entire search tree if we run SA enough

    Acceptance rate depends on quality of best solution (accuracy) and temperature

    Temperature dictates rate of randomness

    Idea: Have temperature relate to num_features and maybe num_instances
    so that we have a better chance of finding a better solution
    Also have temperature decrease at a rate related to num_features and/or num_instances

    Idea: Have temperature relate to quality of results for each search, improve based
    on that -- if results don't meet a certain accuracy standard, initialize temperature
    and rate of change accordingly

    Idea: Have temperature relate to the quality of each feature. Run some tests, record
    quality of features regardless of the state it is being added to. Maybe have the quality
    increase based on the number of features the state has when being added to. Initialize
    temperature and rate of change accordingly

    Idea: Instead of a constant rate of change, have it change depending on quality of
    solution. If major improvement, decrease it more -- might be on right track

    Idea: Use heuristic as described above and give that feature a "boost" in picking it
    when we happen to pick a random solution due to temperature

    Need to read more about it
    """
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
    num_features = len(instances[0]) - 1
    normalized_instances = NormalizeData(instances, num_instances, num_features)
    print("There are %d features with %d instances." % (num_features, num_instances))
    if (alg == "FS"):
        ForwardSelection(normalized_instances, num_instances, num_features)
    elif (alg == "BE"):
        BackwardElimination(normalized_instances, num_instances, num_features)
    else:
        CustomSearch(normalized_instances, num_instances, num_features)

if __name__ == '__main__':
    main()
