# COMP 490 - Lab 3
# Evan Sobkowicz

from indexer import *

class Query:

    # Initializer - generate the index
    def __init__(self):
        i = Indexer()
        self.index = i.index()


    # Token Query
    def token_query(self, term):
        results = list()
        if term in list(self.index.keys()):
            results = list(self.index[term].keys())
        return results


    # AND Query
    def and_query(self, first, second):
        results = list()
        first_ids = self.token_query(first)
        second_ids = self.token_query(second)
        for id in first_ids:
            if id in second_ids:
                results.append(id)
        return results


    # OR Query
    def or_query(self, first, second):
        first_ids = self.token_query(first)
        second_ids = self.token_query(second)
        return first_ids + second_ids


    # Phrase Query
    def phrase_query(self, first, second):
        results = list()
        matches = list()
        and_results = self.and_query(first, second)
        for id in and_results:
            for position in self.index[first][id]:
                for position2 in self.index[second][id]:
                    if position == (position2 - 1):
                        matches.append(id)
        for id in matches:
            if id not in results:
                results.append(id)
        return results


    # Near Query
    def near_query(self, first, second, distance):
        results = list()
        matches = list()
        and_results = self.and_query(first, second)
        for id in and_results:
            for position in self.index[first][id]:
                for position2 in self.index[second][id]:
                    if (position - position2) <= distance:
                        matches.append(id)
        for id in matches:
            if id not in results:
                results.append(id)
        return results
