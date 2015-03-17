# COMP 490 - Lab 5
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *
from random import shuffle


class Evaluator:

    # Initialize Result Accumulators, DB, and Spider
    def __init__(self):
        self.db = WebDB("data/cache.db")
        self.spider = Spider()

    # Evaluate the ranked search engine!
    def evaluate(self):
        print('Evaluating...\n')
        print('P@10', '\t', 'P@R', '\t', 'MAP', '\t', 'AUC', '\t', )
        p10 = list()
        pR = list()
        MAP = list()
        AUC = list()
        q = None
        items = self.get_all_items()
        weightings = ['nnn', 'ltc']
        # TODO: IMPLEMENT RANDOM WEIGHTING?
        for d_weight in weightings:
            for q_weight in weightings:
                q = Query(d_weight, q_weight)
                p10 = []
                pR = []
                MAP = []
                AUC = []
                for item_type in items.keys():
                    for item in items[item_type]:
                        # Run the query for the item
                        tokens = self.spider.tokenize(item)
                        query_results = q.score_query(tokens, False)                  # list() of doc ids
                        # print(item) # FOR DEBUGGING

                        # Set up the True/False list for evaluation
                        data = self.get_data(item, query_results)
                        # print(data) # FOR DEBUGGING

                        # Precision @ 10
                        p10.append(self.precision_x(10, data))

                        # Precision @ R
                        relevant = len(self.db.lookupUrlsForItem(item, item_type)) # Relevant Documents
                        if relevant > 0:
                            # TODO: Fix 'pirates' item lookup (shouldn't need if statement)
                            pR.append(self.precision_x(relevant, data))

                        # Average Precision
                        MAP.append(self.avg_precision(data))

                        # Area Under Curve
                        AUC.append(self.area_under_curve(data))

                weight_type = d_weight + '.' + q_weight
                self.display_results(weight_type, p10, pR, MAP, AUC)

    # Display Evaluation Results
    def display_results(self, weight, p10, pR, MAP, AUC):
        print('Evaluating:', weight)
        print(self.avg(p10), '\t', self.avg(pR), '\t', self.avg(MAP), '\t', self.avg(AUC), '\t', )

    # Return the rounded average of a list of numbers
    def avg(self, nums):
        return round(sum(nums)/len(nums), 2)

    # Create True/False List from doc_ids
    def get_data(self, original_item, result_ids):
        total_docs = self.db.totalURLs()
        scores = list()
        all_ids = set(self.db.allURLids())
        remaining_ids = list(all_ids.difference(set(result_ids)))
        shuffle(remaining_ids)
        result_ids.extend(remaining_ids)
        for id in result_ids:
            if self.db.lookupItem_ByURLID(id)[0] == original_item:
                scores.append(True)
            else:
                scores.append(False)
        return scores

    # Calculate Precision @ X
    def precision_x(self, x, data):
        score = 0.0
        for i in range(x):
            if data[i]:
                score += 1
        return score/x

    # Calculate Mean Average Precision
    def avg_precision(self, data):
        relevant_count = 1
        total_count = 1
        last_relevant_total_count = 1
        total = 0.0
        for i in range(len(data)):
            if data[i]:
                total += relevant_count/total_count
                relevant_count += 1
                last_relevant_total_count = total_count
            total_count += 1
        return total/last_relevant_total_count

    # Calculate Area Under Curve
    def area_under_curve(self, data):
        # TODO: CHECK THIS MATH!
        total = 0.0
        true_count = 0
        x = 0.0
        y = 0.0
        for i in range(len(data)):
            if data[i]:
                true_count += 1
        false_count = len(data) - true_count
        for i in range(len(data)):
            if data[i]:
                y += (1 / true_count)
            else:
                total += ((1 / false_count) * y)
        return total

    # Return a dict of all items and types from files in '/data/item/'
    def get_all_items(self):
        items = dict() # items = { type : [items] }
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
    # Run the evaluation
    e = Evaluator()
    e.evaluate()



main()