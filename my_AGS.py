import math
import random
import heapq
import copy
import normalize as my_norm
import nearest_neighbor as my_nn

def InitHeap(data, num_instances, num_features, current_set_of_features):
    my_queue = []
    for i in range(1, num_features + 1):
        if (i not in current_set_of_features):
            accuracy = my_nn.OneOutCrossValidation(data, num_instances, current_set_of_features, i)
            feature_pair = (1 - accuracy, i)
            heapq.heappush(my_queue, feature_pair)
    return my_queue

def AdaptiveGreedySearch(data, num_instances, num_features):
    """
    First we perform NN on all features, push them into our
    priority queue with priority: (1 - accuracy) such that
    the most accurate features are in the front.
    After going through all possible features we select
    the best feature to be added to our set.
    Now we begin to add to our set of features one at a time
    from our queue.
    However, if it decreases our best accuracy we will discard it and remake our heap
    and try again. (keep track if we previously remade heap)
    If it fails to find a feature that increases our accuracy, we stop.
    If it does meet the improve, we add it and continue.
    There will also be a maximum limit to the number of features we can have.
    The maximum number of features will be 5.
    """
    current_set_of_features = set()
    best_set_of_features = set()

    recently_reordered = False
    print("-" * 50)
    queue_features = InitHeap(data, num_instances, num_features, current_set_of_features)
    top = heapq.heappop(queue_features)
    best_so_far_accuracy = 1 - top[0]
    feature_to_add = top[1]
    current_set_of_features.add(feature_to_add)
    print("-" * 50)
    print("Initialized set with feature %d with accuracy: %d." % (feature_to_add, best_so_far_accuracy))
    iteration = 1

    while (len(queue_features) != 0 and len(current_set_of_features) < 5):
        print("On iteration %d of the search" % (iteration), "with our set as",\
           current_set_of_features)
        top = heapq.heappop(queue_features)
        feature_to_add = top[1]
        accuracy = my_nn.OneOutCrossValidation(data, num_instances, current_set_of_features,\
            feature_to_add)
        if (accuracy < best_so_far_accuracy):
            if (recently_reordered):
                print("*** Could not find suitable feature, stopping here.")
                print("-" * 50)
                break
            print("*** Next feature does NOT improve accuracy, reinitializing heap with new set.")
            print("-" * 50)
            queue_features = InitHeap(data, num_instances, num_features, current_set_of_features)
            recently_reordered = True
        else:
            print("On iteration %d of the search adding feature %d gives us accuracy: %f" \
                % (iteration, feature_to_add, accuracy))
            print("-" * 50)
            current_set_of_features.add(feature_to_add)
            best_so_far_accuracy = accuracy
            # Only allow remaking heap once if commented
            # recently_reordered = False
        iteration += 1
    print("Best set of features to use: ", current_set_of_features, "with accuracy", best_so_far_accuracy)



