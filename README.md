# Feature Selection
CS170 - Intro to Artificial Intelligence project.

Given a data set with two classes, the program will find the best features suited for classification.
Classification will be done with the nearest neighbor algorithm and tested with one-out cross validation.
It includes forward selection, backward elimination, and a custom search that should be more fast or optimal than the previous two.

## Forward Selection
Start with 0 features, add one at a time with a greedy search for best accuracy.

## Backward Elimination
Start with n features, remove one at a time with a greedy search for best accuracy.

## Custom Search
This custom search uses simulated annealing.
It starts with a random single feature and moves to random neighboring state, meaning it adds one random feature.
Depending on the temperature and quality of the solution it may or may not reject the feature.
If it does reject, it will find another random feature to add.
There is a threshold for a minimum accuracy the state has to meet to be considered for acceptance
since from my observations features with less than 70% accuracy tend to be just flat out bad.
If it does NOT meet it, we will stop there and assume any other features are just as bad.

The search also can be run a number of times depending on user input.
The search is quicker compared to the other two searches BUT it does depend on how many times you run SA.
However, you will sacrifice speed for performance.
The search may find a better solution due to the randomness of SA.
In this case, you will sacrifice performance for speed.
In practice SA does tend to give better results if the data sets used have a distribution with many local maximums
but for the data sets used in this project, it might not be the case.
