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
def print_result(count, id):
    url, docType, title = db.lookupCachedURL_byID(id)
    item, type = db.lookupItem_ByURLID(id)
    print(str(count) + ".\t\t", title)
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


# Main Search Engine Class
def main():
    print("Loading...")
    q = Query()
    query = ""
    print_welcome()
    document_type = input("Please enter SMART variant for documents: ")
    query_type = input("Please enter SMART variant for queries: ")
    print("Loading Index...")
    query_weight_scheme = input("Query Weighting Scheme: ")
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
            for result in results:
                item = print_result(count, result)
                items.append(item)
                count += 1
            print_stats(count, items)


main()