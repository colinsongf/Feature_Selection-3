import math
import random
import queue
import normalize as my_norm
import nearest_neighbor as my_nn

def AdaptiveGreedySearch(data, num_instances, num_features):
    """
    First we perform NN on all features, push them into our
    priority queue with priority: (1 - accuracy) such that
    the most accurate features are in the front.
    After going through all possible features we select
    the best feature to be added to our set.
    Now we begin to add to our set of features one at a time
    from our queue.
    However, there is a minimum accuracy the set must meet when
    feature A is being added to our set.
    If it does not meet the minimum, we discard our queue and reevaluate
    the features with our current set of features in mind and make a new queue.
    The minimum accuracy will be (current_accuracy - X).
    Where X will steadily increase such that it becomes less forgivable
    as we begin to add more features, where X is 0.3.
    If it does meet the minimum we add it and continue.
    There will also be a maximum limit to the number of features we can have.
    The maximum number of features will be 5.
    """
    current_set_of_features = set()
    queue_features = queue.PriorityQueue()
    best_so_far_accuracy = 0
    print("-" * 50)



