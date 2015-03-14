# COMP 490 - Lab 5
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *


class Evaluator:

    def evaluate(self):
        items = self.get_all_items()
        weightings = ['nnn', 'ltc']
        for d_weight in weightings:
            # TODO: calculate index for all documents
            for q_weight in weightings:
                q = Query(d_weight, q_weight)
                for item in items:
                    print(item)
                    # TODO: calculate and store AP, R-Precision, Precision@10, AUC for query
        # TODO: print out mean of 4 evaluation metrics


    # Return a list of all items from files in '/data/item/'
    def get_all_items(self):
        items = list()
        for t in self.get_item_types():
            items.extend(self.get_items_by_type(t))
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