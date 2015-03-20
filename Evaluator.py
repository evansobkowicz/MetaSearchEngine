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


    '''
    EVALUATIONS
    ------------------------------------------------------------------------
    '''

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
                # Initialize the Query for the weightings
                q = Query(d_weight, q_weight)
                p10 = []
                pR = []
                MAP = []
                AUC = []
                # Loop over item types and items
                for item_type in items.keys():
                    for item in items[item_type]:
                        # Run the query for the item
                        tokens = self.spider.tokenize(item)
                        query_results = q.score_query(tokens, False)                  # list() of doc ids

                        # Set up the True/False list & relevant doc count for evaluation
                        relevant = len(self.db.lookupUrlsForItem(item, item_type))
                        data = self.get_data(item, query_results)

                        if relevant < 1:
                            print(item)

                        # Precision @ 10
                        p10.append(self.precision_x(10, data))

                        # Precision @ R
                        pR.append(self.precision_x(relevant, data))

                        # Average Precision
                        MAP.append(self.avg_precision(data))

                        # Area Under Curve
                        AUC.append(self.area_under_curve(data))

                # Display the results
                weight_type = d_weight + '.' + q_weight
                self.display_results(weight_type, p10, pR, MAP, AUC)

        # Run the Random Evaluation
        self.random_eval(items)

    # Random Evaluation
    def random_eval(self, items):
        p10 = list()
        pR = list()
        MAP = list()
        AUC = list()
        # Initialize the Query for the weightings
        for item_type in items.keys():
            for item in items[item_type]:
                # Set up the True/False list & relevant doc count for evaluation
                relevant = len(self.db.lookupUrlsForItem(item, item_type))
                data = self.random_list(relevant)

                # Precision @ 10
                p10.append(self.precision_x(10, data))

                # Precision @ R
                pR.append(self.precision_x(relevant, data))

                # Average Precision
                MAP.append(self.avg_precision(data))

                # Area Under Curve
                AUC.append(self.area_under_curve(data))

        # Display the results
        self.display_results('Random', p10, pR, MAP, AUC)


    '''
    RESULTS DISPLAY
    ------------------------------------------------------------------------
    '''

    # Display Evaluation Results
    def display_results(self, weight, p10, pR, MAP, AUC):
        print('Evaluating:', weight)
        print(self.avg(p10), '\t', self.avg(pR), '\t', self.avg(MAP), '\t', self.avg(AUC), '\t', )


    '''
    DATA LIST GENERATION
    ------------------------------------------------------------------------
    '''

    # Create True/False List from doc_ids
    def get_data(self, original_item, result_ids):
        total_docs = self.db.totalURLs()
        scores = list()
        all_ids = set(self.db.allURLids())
        remaining_ids = list(all_ids.difference(set(result_ids)))
        shuffle(remaining_ids)
        result_ids.extend(remaining_ids)
        for id in result_ids:
            if self.db._unquote(self.db.lookupItem_ByURLID(id)[0]) == original_item:
                scores.append(True)
            else:
                scores.append(False)
        return scores

    # Generate Random List of Data (True count = relevant_count)
    def random_list(self, relevant_count):
        results = list()
        total_docs = self.db.totalURLs()
        for i in range(relevant_count):
            results.append(True)
        for i in range(total_docs - relevant_count):
            results.append(False)
        shuffle(results) # Randomize
        return results


    '''
    CALCULATIONS
    ------------------------------------------------------------------------
    '''

    # Calculate Precision @ X
    def precision_x(self, x, data):
        score = 0.0
        for i in range(x):
            if data[i]:
                score += 1
        return score/x

    # Calculate Mean Average Precision
    def avg_precision(self, data):
        relevant_count = 0
        total_count = 0
        total = 0.0
        for i in range(len(data)):
            total_count += 1
            if data[i]:
                relevant_count += 1
                total += relevant_count/total_count
        if relevant_count == 0:
            return 0
        return total/relevant_count

    # Calculate Area Under Curve
    def area_under_curve(self, data):
        total = 0.0
        true_count = 0
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

    # HELPER FUNCTION: Return the rounded average of a list of numbers
    def avg(self, nums):
        return round(sum(nums)/len(nums), 2)


    '''
    ITEM GETTERS
    ------------------------------------------------------------------------
    '''

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


    # ids = [347, 380, 287, 328, 339, 286, 171, 118, 241, 161, 201, 292, 272, 168, 342, 262, 146, 123, 131, 136, 127, 135, 266, 322, 22, 12, 372, 285, 331, 23, 355, 46, 133, 197, 34, 362, 264, 382, 306, 27, 207, 177, 28, 265, 13, 314, 296, 194, 155, 256, 142, 226, 71, 209, 156, 157, 158, 159, 160, 176, 312, 323, 150, 281, 345, 62, 145, 117, 100, 188, 263, 199, 187, 346, 31, 1, 364, 54, 325, 74, 53, 343, 374, 239, 41, 111, 384, 375, 167, 42, 152, 52, 189, 72, 173, 373, 237, 315, 247, 25, 24, 276, 198, 383, 233, 205, 124, 125, 235, 344, 166, 236, 137, 283, 96, 154, 61, 26, 87, 274, 326, 208, 333, 14, 216, 217, 218, 219, 220, 48, 214, 82, 358, 190, 259, 386, 332, 308, 227, 385, 86, 132, 299, 4, 193, 365, 318, 359, 58, 376, 278, 212, 18, 273, 348, 252, 309, 297, 59, 324, 313, 7, 9, 172, 8, 84, 327, 93, 334, 140, 6, 130, 316, 134, 379, 63, 109, 244, 361, 17, 30, 148, 95, 91, 83, 147, 320, 69, 151, 64, 387, 112, 38, 101, 10, 107, 40, 50, 200, 251, 45, 70, 349, 44, 114, 356, 222, 192, 231, 234, 261, 32, 181, 19, 141, 29, 275, 20, 122, 67, 119, 39, 368, 68, 335, 75, 97, 221, 149, 366, 288, 57, 138, 186, 128, 37, 126, 180, 76, 242, 79, 80, 279, 211, 162, 5, 202, 293, 102, 103, 104, 105, 106, 47, 230, 90, 88, 66, 116, 363, 129, 282, 350, 16, 77, 33, 78, 196, 319, 113, 36, 99, 56, 85, 249, 360, 232, 370, 144, 357, 98, 238, 255, 11, 267, 260, 277, 307, 377, 179, 294, 390, 228, 35, 378, 43, 250, 110, 310, 170, 295, 3, 164, 229, 163, 269, 298, 248, 329, 120, 352, 185, 290, 178, 210, 21, 139, 203, 353, 92, 351, 336, 115, 354, 49, 153, 184, 321, 174, 245, 183, 224, 253, 223, 305, 243, 108, 257, 169, 240, 2, 289, 303, 15, 94, 300, 311, 304, 369, 389, 55, 330, 73, 89, 388, 337, 81, 175, 121, 143, 195, 204, 301, 284, 65, 302, 165, 213, 371, 182, 206, 225, 246, 254, 291, 215, 258, 60, 51, 280, 317, 338, 268, 367, 381, 340, 271, 341, 191, 270]
    #
    # for id in ids:
    #     print(e.db._unquote(e.db.lookupItem_ByURLID(id)[0]))


    # TEST SET
    # a = [True, False, True, False, True, False, False, False]
    # b = [False, True, True, True, False, False, False, False]
    # print(e.precision_x(1, b))


main()