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
For my custom search, I plan to use simulated annealing paired with the use of a heuristic.
The heuristic favors selecting the second best feature of the previous search while searching the current features.
It may be faster and better.
If I'm too lazy, I'll drop the heuristic which also makes it better, but maybe slower.
