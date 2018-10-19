from math import *
import numpy as np


class Similarity():

    @staticmethod
    def euclidean_distance(x, y):
        # print("Usando a distancia euclidana")
        print(x, y)
        return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

    @staticmethod
    def manhattan_distance(x, y):
        return sum(abs(a - b) for a, b in zip(x, y))

    def square_rooted(x):
        return round(sqrt(sum([a * a for a in x])), 3)

    @staticmethod
    def jaccard_similarity(x, y):
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)

    @staticmethod
    def chi2_distance(histA, histB, eps=1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                          for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d
