# COMP 490 - Lab 3
# Evan Sobkowicz

from indexer import *

class Query:

    def __init__(self):
        i = Indexer()
        self.index = i.index()


    def token_query(self, term):
        results = list()
        if term in list(self.index.keys()):
            results = list(self.index[term].keys())
        return results


    def and_query(self, first, second):
        results = list()
        first_ids = list()
        second_ids = list()
        if first in list(self.index.keys()):
            first_ids = list(self.index[first].keys())
        if second in list(self.index.keys()):
            second_ids = list(self.index[second].keys())
        for fid in first_ids:
            if fid in second_ids:
                results.append(fid)
        return results


    def or_query(self, first, second):
        first_ids = list()
        second_ids = list()
        if first in list(self.index.keys()):
            first_ids = list(self.index[first].keys())
        if second in list(self.index.keys()):
            second_ids = list(self.index[second].keys())
        return first_ids + second_ids


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


    def near_query(self, first, second):
        results = list()
        # TODO
        return results
