from pprint import pprint
import math
import random
import normalize as my_norm
import nearest_neighbor as my_nn

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

def ForwardSelection(data, num_instances, num_features):
    current_set_of_features = set()
    best_so_far_accuracy = 0
    print("-" * 50)
    for i in range(num_features):
        print("On %d level of the search tree" % (i+ 1), "with our set as", current_set_of_features)
        feature_to_add = -1
        for j in range(1, num_features + 1):
            if (j not in current_set_of_features):
                accuracy = my_nn.OneOutCrossValidation(data, num_instances, current_set_of_features, j)
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_add = j
        if (feature_to_add > 0):
            current_set_of_features.add(feature_to_add)
            print("On %d level of the search tree, adding feature %d gives accuracy: %f" \
            % ((i+1), feature_to_add, best_so_far_accuracy))
            print("-" * 50)
        else:
            print("*** NOTE: Accuracy decreasing, stopping here.")
            break
    print("-" * 50)
    print("Best set of features to use: ", current_set_of_features, "with accuracy", best_so_far_accuracy)

def BackwardElimination(data, num_instances, num_features):
    """
    To remove feature X, pass in -X to OneOutCrossValidation
    """
    current_set_of_features = set(i+1 for i in range(0, num_features))
    best_so_far_accuracy = 0
    print("-" * 50)
    for i in range(num_features):
        print("On level %d of the search tree" % (i+1), "with our set as", current_set_of_features)
        feature_to_remove = -1
        for j in range(1, num_features + 1):
            if (j in current_set_of_features):
                accuracy = my_nn.OneOutCrossValidation(data, num_instances, current_set_of_features, (-1 *j))
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_remove = j
        if (feature_to_remove > 0):
            current_set_of_features.remove(feature_to_remove)
            print("On level %d of the search tree, removing feature %d gives accuracy: %f" \
                % ((i+1), feature_to_remove, best_so_far_accuracy))
            print("-" * 50)
        else:
            print("*** NOTE: Accuracy decreasing, stopping here.")
            break
    print("-" * 50)
    print("Best set of features to use:", current_set_of_features,"with accuracy", best_so_far_accuracy)

def AcceptanceProbability(rand_acc, best_acc, temp):
    natural_log = 2.71828
    accept = pow(natural_log, ((rand_acc - best_acc) / temp))
    return accept

def CustomSearch(data, num_instances, num_features):
    """
    Simple simulated annealing -- referenced ktrinaeg.com and theprojectspot.com
    Instead of making a random initial set with X features, I found it more
    effective to start with a random single feature, because these
    data sets tend to favor fewer features when classifying
    """
    unadded_features = set(i+1 for i in range(0, num_features))
    init_random_feature = random.choice(list(unadded_features))
    current_set_of_features = {init_random_feature}
    best_features = current_set_of_features.copy()
    unadded_features = unadded_features.difference(current_set_of_features)

    minimum_accuracy = 0.70
    temperature = 1.00
    alpha = 0.90
    temp_min = 0.0005
    best_so_far_accuracy = my_nn.OneOutCrossValidation(data, num_instances, current_set_of_features, 0)
    print("-" * 50)

    while (temperature > temp_min and len(unadded_features) > 0):
        level = len(current_set_of_features)
        print("On level %d of the search tree" % (level), "with our set as", current_set_of_features)
        random_feature = random.choice(list(unadded_features))
        accuracy = my_nn.OneOutCrossValidation(data, num_instances, \
            current_set_of_features, random_feature)
        accept = AcceptanceProbability(accuracy, best_so_far_accuracy, temperature)
        if minimum_accuracy > accuracy:
                print("*** NOTE: Accuracy does not meet minimum accuracy, stopping here.")
                break
        if (accept > random.random()):
            current_set_of_features.add(random_feature)
            unadded_features.remove(random_feature)
            print("\t* Accepting feature", random_feature, "to current set.")
            if accuracy > best_so_far_accuracy:
                print("\t** Accepting feature", random_feature, "to best set so far.")
                best_so_far_accuracy = accuracy
                best_features = current_set_of_features.copy()
        else:
            print("\t* Rejecting feature", random_feature, "from set.")
        temperature = temperature * alpha
        print("-" * 50)

    print("Best set of features to use:", best_features, "with accuracy", best_so_far_accuracy)
    return best_features, best_so_far_accuracy

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
    normalized_instances = my_norm.NormalizeData(instances, num_instances, num_features)
    print("There are %d features with %d instances." % (num_features, num_instances))
    if (alg == "FS"):
        ForwardSelection(normalized_instances, num_instances, num_features)
    elif (alg == "BE"):
        BackwardElimination(normalized_instances, num_instances, num_features)
    else:
        SA_num = int(input("Enter the number of times you would like to do simulated annealing:\n"))
        best_features = []
        best_accuracy = 0
        for i in range(1, SA_num + 1):
            print("**** On the %dth simulated annealing search... ****" % i)
            print("-" * 50)
            features, accuracy = CustomSearch(normalized_instances, num_instances, num_features)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_features = features.copy()
            print("-" * 50)
        print("Ending simulated annealing with features", best_features, "and accuracy", best_accuracy)

if __name__ == '__main__':
    main()
