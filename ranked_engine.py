# COMP 490 - Lab 4
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *
from collections import Counter


# Initialize
db = WebDB("data/cache.db")
spider = Spider()


# Get and return user input
def get_input():
    return input("Enter Query or 'QUIT': ")


# Print Welcome Message
def print_welcome():
    print("\n\n\nWelcome to Evan's Boolean Search Engine!")
    print("Supported SMART variants: [n,l][n,t][n,c] (default is 'ltc')\n")


# Print Search Results Heading
def print_results_heading(query):
    print(" ")
    print("---------------------------------------------------------------------------------")
    print("SEARCH RESULTS: ", query)
    print("---------------------------------------------------------------------------------")
    print(" ")


# Print A Result
def print_result(count, id, score):
    url, docType, title = db.lookupCachedURL_byID(id)
    item, type = db.lookupItem_ByURLID(id)
    print(str(count) + ".\t\t", title, " (" + str(score) + ")")
    print("\t\t", url)
    print("\t\t", type + ": " + item)
    print(" ")
    return item


# Print Statistics
def print_stats(count, items):
    words_to_count = (term for term in items if term[:1].isupper())
    c = Counter(words_to_count)
    print("\n----------------------------------------------------------\n")
    print(count-1, "Results Found.")
    print("Most Frequent Items:")
    for term, num in c.most_common(3):
        print("\t" + term + ": " + str(num))
    print("\n----------------------------------------------------------\n")


# SMART Notation Variants
#       l = 1 + log(tf)
#       t = log(N/df)
#       c = (cos) = w / sqrt(Sum(w^2))
def get_variants():
    document = input("Please enter SMART variant for documents: ")
    query = input("Please enter SMART variant for queries: ")
    weight_scheme = input("Query Weighting Scheme: ")
    return document, query, weight_scheme


# TODO: Output scores on result titles and top items (summed from results)
# Main Search Engine Class
def main():
    print("Loading...")
    query = ""
    print_welcome()
    document_type, query_type, query_weight_scheme = get_variants()
    q = Query(document_type, query_type, query_weight_scheme)
    print("Loading Index...")
    while query != "QUIT":
        query = get_input()
        if query == "QUIT":
            print("Goodbye!")
            break
        tokens = spider.tokenize(query)
        results = q.score_query(tokens)
        print_results_heading(query)
        if not results:
            print("***\tNo results found.\t***")
        else:
            count = 1
            items = list()
            for result_id, result_score in results.items():
                item = print_result(count, result_id, result_score)
                items.append(item)
                count += 1
            print_stats(count, items)


main()