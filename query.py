from indexer import *

class Query:

    def __init__(self):
        i = Indexer()
        self.index = i.index()


    def token_query(self, term):
        if term in list(self.index.keys()):
            return list(self.index[term].keys())
        return 0


    def and_query(self, first, second):
        if first in list(self.index.keys()):
            first_ids = list(self.index[first].keys())
        if second in list(self.index.keys()):
            second_ids = list(self.index[second].keys())
        results = list()
        for fid in first_ids:
            if fid in second_ids:
                results.append(fid)
        return results


    def or_query(self, first, second):
        if first in list(self.index.keys()):
            first_ids = list(self.index[first].keys())
        if second in list(self.index.keys()):
            second_ids = list(self.index[second].keys())
        return first_ids + second_ids


    def phrase_query(self, first, second):
        return 0


    def near_query(self, first, second):
        return 0
