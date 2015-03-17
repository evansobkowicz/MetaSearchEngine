# COMP 490 - Lab 5
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *


class Evaluator:

    def __init__(self):
        self.db = WebDB("data/cache.db")
        self.spider = Spider()

    # TODO: Fix pirates item lookup
    def evaluate(self):
        items = self.get_all_items()
        weightings = ['nnn', 'ltc']
        q = None
        for d_weight in weightings:
            for q_weight in weightings:
                q = Query(d_weight, q_weight)
                for item_type in items.keys():
                    for item in items[item_type]:
                        tokens = self.spider.tokenize(item)
                        query_results = q.score_query(tokens, False)                  # list() of doc ids
                        item_results = self.db.lookupUrlsForItem(item, item_type)     # list() of doc ids
                        print(item_results)
                        print(query_results)
                        # TODO: calculate and store AP, R-Precision, Precision@10, AUC for query
        # TODO: print out mean of 4 evaluation metrics



    # Return a dict of all items and types from files in '/data/item/'
    #   Structure items = { type : [items] }
    def get_all_items(self):
        items = dict()
        for t in self.get_item_types():
            items[t] = self.get_items_by_type(t)
        return items


    # Get item types from file names in item directory
    def get_item_types(self):
        types = list()
        path = "data/item/"
        dirs = os.listdir(path)
        for dir in dirs:
            type = dir.strip('.txt')
            types.append(type)
        return types

    # Read items from text file into a list
    def get_items_by_type(self, type):
        results = list()
        path = "data/item/" + type + ".txt"
        f = open(path, "r")
        lines = f.readlines()
        for line in lines:
            clean_line = line.strip('\n')
            results.append(clean_line)
        f.close()
        return results


def main():
    e = Evaluator()
    e.evaluate()



main()